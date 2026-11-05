#!/usr/bin/env python3
"""
Generate a Google Merchant Center Promotions feed from live Shopify discount data.

Usage:
    export SHOPIFY_STORE_DOMAIN=your-store.myshopify.com
    export SHOPIFY_ADMIN_ACCESS_TOKEN=shpat_xxx
    python3 scripts/generate_promotions_feed.py

What it does:
    1. Queries the Shopify Admin GraphQL API for ACTIVE automatic discounts
       (Basic, Buy X Get Y, Free Shipping).
    2. Reads the current feed (--out-tsv) and keeps every row that hasn't
       ended yet, unchanged.
    3. For each active discount whose latest row ends within --renew-days
       (or that has no row yet), adds a new row with a new promotion_id.
    4. Writes the TSV, and updates the xlsx template in place so its header
       styling and Google's notes are kept.

Why a new promotion_id for each period:
    Google doesn't let a promotions data source edit a promotion once it has
    been approved, and a promotion's start date can never change. To keep an
    offer running you submit a new promotion, with a new ID, before the old
    one ends. New IDs are the base ID plus the date the new row starts
    displaying, e.g. TALISMAN_SIEVE_SCREEN_20261203.

    specific_products promotions only work if the matching products in the
    product feed carry the same promotion_id, so every new ID has to be
    added there too. The script prints the new IDs it creates.

Dates (in --timezone, the store's time zone):
    - promotion_effective_dates starts today, so Google can review the new row
      before it displays.
    - promotion_display_dates starts the second after the previous row ends,
      so there is no gap. For an offer with no current row it starts
      --review-lead-days after today, which gives Google time to review it.
    - Both end --default-duration-days after the display start, or when the
      Shopify discount ends if that's sooner. Neither ever runs more than 183
      days past the effective start, Google's maximum promotion length.

Promotion IDs and titles:
    --config (default feeds/promotions_config.json) maps a Shopify discount ID
    to the base promotion_id and long_title to use. A discount with no entry
    gets an ID built from its Shopify title. Never change a base
    promotion_id once Google has seen it.

Why only automatic discounts:
    Shopify code-based discounts on this store include a large number of
    one-off customer-service courtesy codes (named after individual customers)
    and expired seasonal codes. Those are not public storefront promotions and
    must never be published to a public Google Shopping feed. Automatic
    discounts apply to every shopper at checkout with no code, so they are the
    set that is actually safe to treat as "public promotions" by default.

    To publish a real public promo code, add its row to the TSV by hand. The
    script keeps rows it doesn't manage until their end date passes.
"""
import argparse
import csv
import json
import os
import re
import sys
import urllib.error
import urllib.request
from copy import copy
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# Shopify supports each Admin API version for about a year; bump this when
# Shopify announces the version's end of support.
API_VERSION = "2026-10"

# Google rejects promotions that run longer than this from their effective start.
GOOGLE_MAX_PROMOTION_DAYS = 183
GOOGLE_MAX_ID_LENGTH = 50
GOOGLE_MAX_LONG_TITLE_LENGTH = 60

FEED_COLUMNS = [
    "promotion_id",
    "product_applicability",
    "long_title",
    "promotion_effective_dates",
    "promotion_display_dates",
    "redemption_channel",
    "offer_type",
    "generic_redemption_code",
    "promotion_destination",
]

SUPPORTED_DISCOUNT_TYPES = {
    "DiscountAutomaticBasic",
    "DiscountAutomaticBxgy",
    "DiscountAutomaticFreeShipping",
}

DISCOUNTS_QUERY = """
query AutomaticDiscounts($cursor: String) {
  discountNodes(first: 100, after: $cursor, query: "method:automatic AND status:active") {
    nodes {
      id
      discount {
        __typename
        ... on DiscountAutomaticBasic {
          title status startsAt endsAt
          customerGets { items { __typename } }
        }
        ... on DiscountAutomaticBxgy { title status startsAt endsAt }
        ... on DiscountAutomaticFreeShipping { title status startsAt endsAt }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
"""

# A renewed row's ID is the base ID plus its display start date.
DATED_ID_SUFFIX = re.compile(r"_\d{8}$")


def shopify_graphql(domain, token, query, variables=None, api_version=API_VERSION):
    url = f"https://{domain}/admin/api/{api_version}/graphql.json"
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": token,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Shopify API error {e.code}: {e.read().decode()}")
    if "errors" in payload:
        raise SystemExit(f"Shopify GraphQL errors: {payload['errors']}")
    return payload["data"]


def fetch_active_automatic_discounts(domain, token, api_version=API_VERSION):
    """Return (discounts, skipped_app_count). Each discount is a plain dict."""
    discounts = []
    skipped_app = 0
    cursor = None
    while True:
        data = shopify_graphql(domain, token, DISCOUNTS_QUERY, {"cursor": cursor}, api_version)
        conn = data["discountNodes"]
        for node in conn["nodes"]:
            d = node["discount"]
            kind = d.get("__typename")
            if kind not in SUPPORTED_DISCOUNT_TYPES:
                if kind == "DiscountAutomaticApp":
                    skipped_app += 1
                continue
            if d.get("status") != "ACTIVE":
                continue
            items = ((d.get("customerGets") or {}).get("items") or {}).get("__typename")
            discounts.append({
                "id": node["id"],
                "type": kind,
                "title": d["title"],
                "startsAt": d["startsAt"],
                "endsAt": d.get("endsAt"),
                "all_items": items == "AllDiscountItems",
            })
        if not conn["pageInfo"]["hasNextPage"]:
            break
        cursor = conn["pageInfo"]["endCursor"]
    return discounts, skipped_app


def slugify_id(title, max_len=40):
    slug = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_").upper()
    return slug[:max_len] or "PROMO"


def base_promotion_id(promotion_id):
    return DATED_ID_SUFFIX.sub("", promotion_id)


def parse_datetime(value):
    return datetime.fromisoformat(value.strip().replace("Z", "+00:00"))


def parse_interval(value):
    """Parse Google's 'start/end' ISO 8601 interval. Returns None if blank or unreadable."""
    if not value or "/" not in value:
        return None
    start, end = value.split("/", 1)
    try:
        return parse_datetime(start), parse_datetime(end)
    except ValueError:
        return None


def format_interval(start, end):
    return f"{start.isoformat(timespec='seconds')}/{end.isoformat(timespec='seconds')}"


def row_end(row):
    """When a row stops showing: its display end, falling back to its effective end."""
    for col in ("promotion_display_dates", "promotion_effective_dates"):
        interval = parse_interval(row.get(col, ""))
        if interval:
            return interval[1]
    return None


def load_config(path):
    if not path or not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        config = json.load(f)
    return {k: v for k, v in config.items() if not k.startswith("_")}


def load_existing_rows(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return [
            {col: (row.get(col) or "") for col in FEED_COLUMNS}
            for row in csv.DictReader(f, delimiter="\t")
            if (row.get("promotion_id") or "").strip()
        ]


def build_feed(discounts, existing_rows, config, now, tz, duration_days=90,
               review_lead_days=3, renew_days=30, destination="Shopping_ads"):
    """Merge current feed rows with active Shopify discounts.

    Returns (rows, new_ids, notices).
    """
    notices = []
    today_start = datetime.combine(now.astimezone(tz).date(), time.min, tzinfo=tz)

    active = {}  # base promotion_id -> (discount, config entry)
    for d in discounts:
        entry = config.get(d["id"], {})
        base = entry.get("promotion_id") or slugify_id(d["title"])
        if base in active:
            notices.append(
                f"'{d['title']}' maps to promotion_id {base}, which another discount "
                f"already uses; skipped it. Give it its own promotion_id in the config."
            )
            continue
        active[base] = (d, entry)
    configured_bases = {e["promotion_id"] for e in config.values() if e.get("promotion_id")}

    # Carry over current rows unchanged: Google won't accept edits to approved ones.
    kept = []
    for row in existing_rows:
        pid = row["promotion_id"].strip()
        base = base_promotion_id(pid)
        end = row_end(row)
        if end is None:
            notices.append(f"Kept {pid} unchanged: couldn't read its dates. Check it by hand.")
            kept.append(row)
            continue
        if end <= now:
            notices.append(f"Removed {pid}: it ended {end.date().isoformat()}.")
            continue
        if base in configured_bases and base not in active:
            notices.append(f"Removed {pid}: its Shopify discount is no longer active.")
            continue
        if base not in active:
            notices.append(
                f"Kept {pid} unchanged: it doesn't match an active automatic Shopify "
                f"discount. Remove it by hand if the offer has ended."
            )
        kept.append(row)

    kept_ids = {row["promotion_id"] for row in kept}
    new_rows = []
    for base, (d, entry) in sorted(active.items()):
        ends = [e for e in (row_end(r) for r in kept if base_promotion_id(r["promotion_id"]) == base) if e]
        latest_end = max(ends) if ends else None
        if latest_end and latest_end - now > timedelta(days=renew_days):
            continue

        effective_start = max(today_start, parse_datetime(d["startsAt"]).astimezone(tz))
        if latest_end:
            display_start = max(effective_start, (latest_end + timedelta(seconds=1)).astimezone(tz))
        else:
            display_start = effective_start + timedelta(days=review_lead_days)

        last_day = display_start.date() + timedelta(days=duration_days - 1)
        end = datetime.combine(last_day, time(23, 59, 59), tzinfo=tz)
        synthetic_end = True
        if d.get("endsAt"):
            shopify_end = parse_datetime(d["endsAt"]).astimezone(tz)
            if shopify_end < end:
                end, synthetic_end = shopify_end, False
        google_cap = effective_start + timedelta(days=GOOGLE_MAX_PROMOTION_DAYS) - timedelta(seconds=1)
        if end > google_cap:
            end = google_cap
        if end <= display_start:
            notices.append(
                f"No new row for '{d['title']}': the Shopify discount ends before a new "
                f"promotion could start."
            )
            continue

        promotion_id = f"{base}_{display_start:%Y%m%d}"
        if promotion_id in kept_ids:
            notices.append(f"{promotion_id} is already in the feed; left it as is.")
            continue
        long_title = entry.get("long_title") or d["title"]
        if len(promotion_id) > GOOGLE_MAX_ID_LENGTH:
            notices.append(f"{promotion_id} is longer than Google's {GOOGLE_MAX_ID_LENGTH}-character limit.")
        if len(long_title) > GOOGLE_MAX_LONG_TITLE_LENGTH:
            notices.append(
                f"long_title for {promotion_id} is {len(long_title)} characters; "
                f"Google allows {GOOGLE_MAX_LONG_TITLE_LENGTH}."
            )
        if synthetic_end:
            notices.append(
                f"'{d['title']}' has no end date in Shopify, so {promotion_id} ends "
                f"{end.date().isoformat()}. Re-run this script within {renew_days} days "
                f"of that date to renew it."
            )
        new_rows.append({
            "promotion_id": promotion_id,
            "product_applicability": entry.get("product_applicability")
            or ("all_products" if d.get("all_items") else "specific_products"),
            "long_title": long_title,
            "promotion_effective_dates": format_interval(effective_start, end),
            "promotion_display_dates": format_interval(display_start, end),
            "redemption_channel": "online",
            "offer_type": "no_code",
            "generic_redemption_code": "",
            "promotion_destination": destination,
        })

    def sort_key(row):
        interval = parse_interval(row["promotion_effective_dates"])
        start = interval[0].timestamp() if interval else 0
        return base_promotion_id(row["promotion_id"]), start, row["promotion_id"]

    rows = sorted(kept + new_rows, key=sort_key)
    return rows, [r["promotion_id"] for r in new_rows], notices


def write_tsv(rows, path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FEED_COLUMNS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


STYLE_ATTRS = ("font", "fill", "border", "alignment", "protection", "number_format")


def _cell_style(cell):
    return {attr: copy(getattr(cell, attr)) for attr in STYLE_ATTRS}


def write_xlsx(rows, path):
    """Update the data rows of the xlsx template in place, keeping everything else."""
    import openpyxl
    from openpyxl.styles import Font

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    ncols = len(FEED_COLUMNS)
    if os.path.exists(path):
        wb = openpyxl.load_workbook(path)
        ws = wb.active
        header = [ws.cell(row=1, column=c).value for c in range(1, ncols + 1)]
        if header != FEED_COLUMNS:
            raise SystemExit(f"{path}: row 1 isn't the promotions feed header; not overwriting it.")
        # The data block runs from row 2 until the first row with an empty promotion_id.
        old_count = 0
        while ws.cell(row=2 + old_count, column=1).value not in (None, ""):
            old_count += 1
        # New and existing data rows all take the first data row's formatting.
        template = [_cell_style(ws.cell(row=2, column=c)) for c in range(1, ncols + 1)] if old_count else None
        if len(rows) > old_count:
            ws.insert_rows(2 + old_count, len(rows) - old_count)
        elif len(rows) < old_count:
            ws.delete_rows(2 + len(rows), old_count - len(rows))
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        ws.append(FEED_COLUMNS)
        for cell in ws[1]:
            cell.font = Font(bold=True)
        template = None

    for r, row in enumerate(rows, start=2):
        for c, col in enumerate(FEED_COLUMNS, start=1):
            cell = ws.cell(row=r, column=c)
            cell.value = row[col] or None
            if template:
                for attr, value in template[c - 1].items():
                    setattr(cell, attr, copy(value))
    wb.save(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out-tsv", default="feeds/google_merchant_promotions.txt",
                        help="Feed to update. Its current rows are read first (default: %(default)s).")
    parser.add_argument("--out-xlsx", default="feeds/google_merchant_promotions.xlsx")
    parser.add_argument("--config", default="feeds/promotions_config.json",
                        help="Shopify discount ID -> promotion_id/long_title overrides (default: %(default)s).")
    parser.add_argument("--default-duration-days", type=int, default=90,
                        help="How long a new row displays when the Shopify discount has no end date (default: 90).")
    parser.add_argument("--renew-days", type=int, default=30,
                        help="Add a new row when the current one ends within this many days (default: 30).")
    parser.add_argument("--review-lead-days", type=int, default=3,
                        help="Days between effective and display start for a brand-new promotion (default: 3).")
    parser.add_argument("--timezone", default="America/New_York",
                        help="Time zone for promotion dates (default: %(default)s).")
    parser.add_argument("--as-of", type=date.fromisoformat, metavar="YYYY-MM-DD",
                        help="Treat this date as today (for previewing a future run).")
    parser.add_argument("--destination", default="Shopping_ads",
                        help="promotion_destination value (default: Shopping_ads).")
    parser.add_argument("--api-version", default=os.environ.get("SHOPIFY_API_VERSION", API_VERSION),
                        help="Shopify Admin API version (default: %(default)s).")
    args = parser.parse_args()

    if not 1 <= args.default_duration_days <= GOOGLE_MAX_PROMOTION_DAYS:
        parser.error(f"--default-duration-days must be between 1 and {GOOGLE_MAX_PROMOTION_DAYS}.")
    try:
        tz = ZoneInfo(args.timezone)
    except ZoneInfoNotFoundError:
        raise SystemExit(
            f"Unknown time zone '{args.timezone}'. On Windows, install time zone data with: pip install tzdata"
        )
    now = (datetime.combine(args.as_of, time.min, tzinfo=tz) if args.as_of
           else datetime.now(timezone.utc))

    domain = os.environ.get("SHOPIFY_STORE_DOMAIN")
    token = os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN")
    if not domain or not token:
        raise SystemExit(
            "Set SHOPIFY_STORE_DOMAIN and SHOPIFY_ADMIN_ACCESS_TOKEN environment variables first."
        )

    discounts, skipped_app = fetch_active_automatic_discounts(domain, token, args.api_version)
    rows, new_ids, notices = build_feed(
        discounts,
        load_existing_rows(args.out_tsv),
        load_config(args.config),
        now,
        tz,
        duration_days=args.default_duration_days,
        review_lead_days=args.review_lead_days,
        renew_days=args.renew_days,
        destination=args.destination,
    )

    write_tsv(rows, args.out_tsv)
    write_xlsx(rows, args.out_xlsx)

    print(f"Wrote {len(rows)} promotion row(s) to {args.out_tsv} and {args.out_xlsx}")
    if skipped_app:
        print(f"Skipped {skipped_app} app-managed automatic discount(s); add any public ones by hand.")
    for notice in notices:
        print(f"NOTE: {notice}", file=sys.stderr)
    if new_ids:
        print("\nNew promotion IDs. Add each to the promotion_id of the matching products in the "
              "product feed before uploading, or Google will disapprove them:")
        for pid in new_ids:
            print(f"  {pid}")
    else:
        print("No new promotions needed yet.")


if __name__ == "__main__":
    main()
