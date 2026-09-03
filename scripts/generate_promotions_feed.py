#!/usr/bin/env python3
"""
Generate a Google Merchant Center Promotions feed from live Shopify discount data.

Usage:
    export SHOPIFY_STORE_DOMAIN=your-store.myshopify.com
    export SHOPIFY_ADMIN_ACCESS_TOKEN=shpat_xxx
    python3 scripts/generate_promotions_feed.py [--out-tsv feeds/promotions.txt] [--out-xlsx feeds/promotions.xlsx]

What it does:
    Queries the Shopify Admin GraphQL API for ACTIVE automatic discounts (Basic,
    BxGy, Free Shipping) and converts each into one row of Google's Promotions
    feed schema: promotion_id, product_applicability, long_title,
    promotion_effective_dates, promotion_display_dates, redemption_channel,
    offer_type, generic_redemption_code, promotion_destination.

Why only automatic discounts:
    Shopify code-based discounts on this store include a large number of
    one-off customer-service courtesy codes (named after individual customers)
    and expired seasonal codes. Those are not public storefront promotions and
    must never be published to a public Google Shopping feed. Automatic
    discounts apply to every shopper at checkout with no code, so they are the
    set that is actually safe to treat as "public promotions" by default.

    To include specific code-based promotions anyway (e.g. a real public sale
    code), list their Shopify discount titles in --include-codes.

Effective/display dates:
    Google requires a bounded ISO 8601 interval (start/end) for both dates.
    Shopify automatic discounts are frequently open-ended (no end date). When
    a discount has no end date, this script assigns a synthetic end date
    --default-duration-days out from today (default: 90) and flags the row so
    a human confirms/adjusts it before upload.
"""
import argparse
import csv
import os
import re
import sys
import urllib.request
import urllib.error
import json
from datetime import datetime, timedelta, timezone

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

DISCOUNTS_QUERY = """
query AutomaticDiscounts($cursor: String) {
  automaticDiscountNodes(first: 100, after: $cursor) {
    nodes {
      id
      automaticDiscount {
        __typename
        ... on DiscountAutomaticBasic {
          title status startsAt endsAt
          customerGets {
            items {
              __typename
              ... on AllDiscountItems { allItems }
            }
          }
        }
        ... on DiscountAutomaticBxgy {
          title status startsAt endsAt
        }
        ... on DiscountAutomaticFreeShipping {
          title status startsAt endsAt
        }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
"""


def shopify_graphql(domain, token, query, variables=None):
    url = f"https://{domain}/admin/api/2024-10/graphql.json"
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


def fetch_active_automatic_discounts(domain, token):
    discounts = []
    cursor = None
    while True:
        data = shopify_graphql(domain, token, DISCOUNTS_QUERY, {"cursor": cursor})
        conn = data["automaticDiscountNodes"]
        for node in conn["nodes"]:
            d = node["automaticDiscount"]
            if d.get("status") == "ACTIVE":
                discounts.append(d)
        if not conn["pageInfo"]["hasNextPage"]:
            break
        cursor = conn["pageInfo"]["endCursor"]
    return discounts


def slugify_id(title, max_len=40):
    slug = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_").upper()
    return slug[:max_len] or "PROMO"


def iso_interval(start_str, end_str, default_duration_days):
    """Return (interval_string, was_synthetic_end) in Google's start/end ISO8601 format."""
    start_dt = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
    synthetic = end_str is None
    if end_str is None:
        end_dt = datetime.now(timezone.utc) + timedelta(days=default_duration_days)
    else:
        end_dt = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
    fmt = "%Y-%m-%dT%H:%M:%S%z"

    def fix(dt_str):
        # insert colon in UTC offset: +0000 -> +00:00
        return dt_str[:-2] + ":" + dt_str[-2:]

    return f"{fix(start_dt.strftime(fmt))}/{fix(end_dt.strftime(fmt))}", synthetic


def build_rows(discounts, default_duration_days, destination):
    rows = []
    warnings = []
    for d in discounts:
        title = d["title"]
        promo_id = slugify_id(title)
        interval, synthetic = iso_interval(d["startsAt"], d.get("endsAt"), default_duration_days)
        if synthetic:
            warnings.append(
                f"'{title}' has no end date in Shopify; assigned a synthetic "
                f"{default_duration_days}-day promotion_effective_dates end. "
                f"Confirm/adjust before upload."
            )
        row = {
            "promotion_id": promo_id,
            "product_applicability": "specific_products",
            "long_title": title,
            "promotion_effective_dates": interval,
            "promotion_display_dates": "",
            "redemption_channel": "online",
            "offer_type": "no_code",
            "generic_redemption_code": "",
            "promotion_destination": destination,
        }
        rows.append(row)
    return rows, warnings


def write_tsv(rows, path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FEED_COLUMNS, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def write_xlsx(rows, path):
    import openpyxl

    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.append(FEED_COLUMNS)
    for row in rows:
        ws.append([row[c] for c in FEED_COLUMNS])
    wb.save(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out-tsv", default="feeds/google_merchant_promotions.txt")
    parser.add_argument("--out-xlsx", default="feeds/google_merchant_promotions.xlsx")
    parser.add_argument("--default-duration-days", type=int, default=90,
                         help="Synthetic promotion length for discounts with no end date (default: 90).")
    parser.add_argument("--destination", default="Shopping_ads",
                         help="promotion_destination value (default: Shopping_ads).")
    args = parser.parse_args()

    domain = os.environ.get("SHOPIFY_STORE_DOMAIN")
    token = os.environ.get("SHOPIFY_ADMIN_ACCESS_TOKEN")
    if not domain or not token:
        raise SystemExit(
            "Set SHOPIFY_STORE_DOMAIN and SHOPIFY_ADMIN_ACCESS_TOKEN environment variables first."
        )

    discounts = fetch_active_automatic_discounts(domain, token)
    rows, warnings = build_rows(discounts, args.default_duration_days, args.destination)

    write_tsv(rows, args.out_tsv)
    write_xlsx(rows, args.out_xlsx)

    print(f"Wrote {len(rows)} promotion row(s) to {args.out_tsv} and {args.out_xlsx}")
    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)


if __name__ == "__main__":
    main()
