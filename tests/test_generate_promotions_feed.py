"""Tests for scripts/generate_promotions_feed.py. Run: python3 -m unittest discover tests"""
import importlib.util
import os
import tempfile
import unittest
from datetime import date, datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("feedgen", ROOT / "scripts" / "generate_promotions_feed.py")
feedgen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(feedgen)

TZ = ZoneInfo("America/New_York")
TALISMAN = "gid://shopify/DiscountAutomaticNode/1"
BTH = "gid://shopify/DiscountAutomaticNode/2"
CONFIG = {
    TALISMAN: {"promotion_id": "TALISMAN_SIEVE_SCREEN", "long_title": "Free Screen with Talisman Sieve"},
    BTH: {"promotion_id": "BTH_WHEEL_CLAY_DISCOUNT", "long_title": "$45 Off Clay with BTH Wheel"},
}


def discount(gid, title, starts="2024-02-15T16:26:32Z", ends=None, all_items=False):
    return {"id": gid, "type": "DiscountAutomaticBxgy", "title": title,
            "startsAt": starts, "endsAt": ends, "all_items": all_items}


def row(pid, effective, display=""):
    r = {c: "" for c in feedgen.FEED_COLUMNS}
    r.update(promotion_id=pid, product_applicability="specific_products", long_title="t",
             promotion_effective_dates=effective, promotion_display_dates=display,
             redemption_channel="online", offer_type="no_code", promotion_destination="Shopping_ads")
    return r


def on(day):
    return datetime.combine(day, time.min, tzinfo=TZ)


CURRENT = [
    row("TALISMAN_SIEVE_SCREEN", "2026-09-03T00:00:00-04:00/2026-12-02T23:59:59-05:00",
        "2026-09-06T00:00:00-04:00/2026-12-02T23:59:59-05:00"),
    row("BTH_WHEEL_CLAY_DISCOUNT", "2026-09-03T00:00:00-04:00/2026-12-02T23:59:59-05:00",
        "2026-09-06T00:00:00-04:00/2026-12-02T23:59:59-05:00"),
]
ACTIVE = [discount(TALISMAN, "Screen Included With Talisman Sieve"),
          discount(BTH, "$45 off Clay with BTH", starts="2026-03-18T13:26:23Z")]


class BuildFeedTest(unittest.TestCase):
    def build(self, discounts, existing, today, **kw):
        return feedgen.build_feed(discounts, existing, CONFIG, on(today), TZ, **kw)

    def test_renewal_keeps_current_rows_and_adds_seamless_new_ones(self):
        rows, new_ids, _ = self.build(ACTIVE, CURRENT, date(2026, 11, 5))
        self.assertEqual(new_ids, ["BTH_WHEEL_CLAY_DISCOUNT_20261203", "TALISMAN_SIEVE_SCREEN_20261203"])
        self.assertEqual(CURRENT[0], next(r for r in rows if r["promotion_id"] == "TALISMAN_SIEVE_SCREEN"))
        new = next(r for r in rows if r["promotion_id"] == "TALISMAN_SIEVE_SCREEN_20261203")
        self.assertEqual(new["promotion_effective_dates"],
                         "2026-11-05T00:00:00-05:00/2027-03-02T23:59:59-05:00")
        self.assertEqual(new["promotion_display_dates"],
                         "2026-12-03T00:00:00-05:00/2027-03-02T23:59:59-05:00")
        self.assertEqual(new["long_title"], "Free Screen with Talisman Sieve")
        self.assertEqual([r["promotion_id"] for r in rows], [
            "BTH_WHEEL_CLAY_DISCOUNT", "BTH_WHEEL_CLAY_DISCOUNT_20261203",
            "TALISMAN_SIEVE_SCREEN", "TALISMAN_SIEVE_SCREEN_20261203"])

    def test_rerun_is_idempotent(self):
        rows, _, _ = self.build(ACTIVE, CURRENT, date(2026, 11, 5))
        again, new_ids, _ = self.build(ACTIVE, rows, date(2026, 11, 5))
        self.assertEqual(new_ids, [])
        self.assertEqual(again, rows)

    def test_no_renewal_when_current_row_has_time_left(self):
        rows, new_ids, _ = self.build(ACTIVE, CURRENT, date(2026, 10, 1))
        self.assertEqual(new_ids, [])
        self.assertEqual(rows, sorted(CURRENT, key=lambda r: r["promotion_id"]))

    def test_expired_rows_are_dropped_and_a_missed_renewal_restarts_with_review_time(self):
        rows, _, notices = self.build(ACTIVE, CURRENT, date(2026, 12, 10))
        ids = [r["promotion_id"] for r in rows]
        self.assertNotIn("TALISMAN_SIEVE_SCREEN", ids)
        self.assertIn("TALISMAN_SIEVE_SCREEN_20261213", ids)
        self.assertTrue(any("ended 2026-12-02" in n for n in notices))

    def test_row_for_ended_discount_is_removed(self):
        rows, new_ids, notices = self.build(ACTIVE[:1], CURRENT, date(2026, 11, 5))
        self.assertNotIn("BTH_WHEEL_CLAY_DISCOUNT", [r["promotion_id"] for r in rows])
        self.assertEqual(new_ids, ["TALISMAN_SIEVE_SCREEN_20261203"])
        self.assertTrue(any("no longer active" in n for n in notices))

    def test_unmanaged_rows_are_kept_until_they_end(self):
        manual = row("SPRING_SALE_CODE", "2026-11-01T00:00:00-04:00/2027-01-31T23:59:59-05:00")
        rows, _, notices = self.build(ACTIVE, CURRENT + [manual], date(2026, 11, 5))
        self.assertIn(manual, rows)
        self.assertTrue(any("SPRING_SALE_CODE" in n for n in notices))

    def test_new_promotion_gets_review_lead_time(self):
        rows, new_ids, _ = self.build(ACTIVE[:1], [], date(2026, 11, 5))
        self.assertEqual(new_ids, ["TALISMAN_SIEVE_SCREEN_20261108"])
        self.assertEqual(rows[0]["promotion_display_dates"],
                         "2026-11-08T00:00:00-05:00/2027-02-05T23:59:59-05:00")

    def test_never_longer_than_googles_183_days(self):
        rows, _, _ = self.build(ACTIVE[:1], [], date(2026, 11, 5), duration_days=183)
        start, end = feedgen.parse_interval(rows[0]["promotion_effective_dates"])
        self.assertLessEqual((end - start).total_seconds(), 183 * 86400)
        self.assertEqual(end, datetime(2027, 5, 6, 23, 59, 59, tzinfo=TZ))

    def test_shopify_end_date_wins_when_sooner(self):
        d = discount(TALISMAN, "x", ends="2026-12-31T17:00:00Z")
        rows, _, notices = self.build([d], [], date(2026, 11, 5))
        self.assertTrue(rows[0]["promotion_effective_dates"].endswith("/2026-12-31T12:00:00-05:00"))
        self.assertFalse(any("no end date" in n for n in notices))

    def test_unconfigured_discount_uses_slug_and_all_products(self):
        d = discount("gid://shopify/DiscountAutomaticNode/9", "10% off everything!", all_items=True)
        rows, new_ids, _ = self.build([d], [], date(2026, 11, 5))
        self.assertEqual(new_ids, ["10_OFF_EVERYTHING_20261108"])
        self.assertEqual(rows[0]["product_applicability"], "all_products")
        self.assertEqual(rows[0]["long_title"], "10% off everything!")


class FetchTest(unittest.TestCase):
    def test_pages_and_skips_app_discounts(self):
        pages = [
            {"discountNodes": {"nodes": [
                {"id": "a", "discount": {"__typename": "DiscountAutomaticApp"}},
                {"id": "b", "discount": {"__typename": "DiscountAutomaticBasic", "title": "B", "status": "ACTIVE",
                                         "startsAt": "2026-01-01T00:00:00Z", "endsAt": None,
                                         "customerGets": {"items": {"__typename": "AllDiscountItems"}}}},
            ], "pageInfo": {"hasNextPage": True, "endCursor": "c1"}}},
            {"discountNodes": {"nodes": [
                {"id": "c", "discount": {"__typename": "DiscountAutomaticBxgy", "title": "C", "status": "EXPIRED",
                                         "startsAt": "2026-01-01T00:00:00Z", "endsAt": None}},
            ], "pageInfo": {"hasNextPage": False, "endCursor": None}}},
        ]
        cursors = []

        def fake(domain, token, query, variables=None, api_version=None):
            cursors.append(variables["cursor"])
            return pages[len(cursors) - 1]

        original = feedgen.shopify_graphql
        feedgen.shopify_graphql = fake
        try:
            discounts, skipped = feedgen.fetch_active_automatic_discounts("d", "t")
        finally:
            feedgen.shopify_graphql = original
        self.assertEqual(cursors, [None, "c1"])
        self.assertEqual(skipped, 1)
        self.assertEqual([d["id"] for d in discounts], ["b"])
        self.assertTrue(discounts[0]["all_items"])


@unittest.skipUnless(importlib.util.find_spec("openpyxl"), "openpyxl not installed")
class XlsxTest(unittest.TestCase):
    def test_updates_rows_and_keeps_notes_and_formatting(self):
        import openpyxl
        from openpyxl.styles import PatternFill

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "feed.xlsx")
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(feedgen.FEED_COLUMNS)
            ws["A1"].fill = PatternFill("solid", fgColor="FFA4C2F4")
            ws.append(["OLD_1", "specific_products", "t"])
            ws["D2"].fill = PatternFill("solid", fgColor="FFF9CB9C")
            ws.append(["OLD_2", "specific_products", "t"])
            ws["B5"] = "Google note"
            ws.column_dimensions["D"].width = 50
            wb.save(path)

            rows = [row(f"NEW_{i}", "2026-11-05T00:00:00-05:00/2027-03-02T23:59:59-05:00") for i in range(4)]
            feedgen.write_xlsx(rows, path)

            ws = openpyxl.load_workbook(path).active
            self.assertEqual([ws.cell(row=r, column=1).value for r in range(1, 7)],
                             ["promotion_id", "NEW_0", "NEW_1", "NEW_2", "NEW_3", None])
            self.assertEqual(ws["B7"].value, "Google note")
            self.assertEqual(ws["A1"].fill.fgColor.rgb, "FFA4C2F4")
            self.assertEqual(ws["D5"].fill.fgColor.rgb, "FFF9CB9C")
            self.assertEqual(ws.column_dimensions["D"].width, 50)
            self.assertIsNone(ws["H2"].value)

            feedgen.write_xlsx(rows[:1], path)
            ws = openpyxl.load_workbook(path).active
            self.assertEqual(ws["A2"].value, "NEW_0")
            self.assertIsNone(ws["A3"].value)
            self.assertEqual(ws["B4"].value, "Google note")


if __name__ == "__main__":
    unittest.main()
