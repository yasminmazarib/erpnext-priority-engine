import unittest
from app.models.inventory_models import InventoryBin
from app.services.inventory_service import InventoryService


class TestInventoryService(unittest.TestCase):

    # ---------- calculate_priority ----------

    def test_high_priority_inventory(self):
        bin = InventoryBin(
            item_code="ITEM-001",
            warehouse="Main Warehouse",
            actual_qty=250,
            reserved_qty=0
        )

        issue = InventoryService.calculate_priority(bin)

        self.assertIsNotNone(issue)
        self.assertEqual(issue.priority, "HIGH")
        self.assertIn("quantity", issue.reason.lower())

    def test_medium_priority_inventory(self):
        bin = InventoryBin(
            item_code="ITEM-002",
            warehouse="Main Warehouse",
            actual_qty=150,
            reserved_qty=0
        )

        issue = InventoryService.calculate_priority(bin)

        self.assertIsNotNone(issue)
        self.assertEqual(issue.priority, "MEDIUM")

    def test_low_priority_inventory(self):
        bin = InventoryBin(
            item_code="ITEM-003",
            warehouse="Main Warehouse",
            actual_qty=50,
            reserved_qty=0
        )

        issue = InventoryService.calculate_priority(bin)

        self.assertIsNotNone(issue)
        self.assertEqual(issue.priority, "LOW")

    def test_inventory_with_zero_quantity(self):
        bin = InventoryBin(
            item_code="ITEM-004",
            warehouse="WH",
            actual_qty=0,
            reserved_qty=0
        )

        issue = InventoryService.calculate_priority(bin)
        self.assertIsNone(issue)

    def test_calculate_priority_with_none_bin(self):
        issue = InventoryService.calculate_priority(None)
        self.assertIsNone(issue)

    # ---------- get_inventory_issues ----------

    def test_inventory_issues_sorted_by_priority(self):
        bins = [
            InventoryBin("A", "WH", 50),
            InventoryBin("B", "WH", 300),
            InventoryBin("C", "WH", 150),
        ]

        issues = InventoryService.get_inventory_issues(bins)

        self.assertEqual(issues[0].priority, "HIGH")
        self.assertEqual(issues[1].priority, "MEDIUM")
        self.assertEqual(issues[2].priority, "LOW")

    def test_get_inventory_issues_empty_list(self):
        issues = InventoryService.get_inventory_issues([])
        self.assertEqual(issues, [])

    # ---------- _to_inventory_bin ----------

    def test_to_inventory_bin_from_dict(self):
        raw = {
            "item_code": "ITEM-100",
            "warehouse": "WH",
            "actual_qty": 120,
            "reserved_qty": 10
        }

        bin_obj = InventoryService._to_inventory_bin(raw)

        self.assertIsNotNone(bin_obj)
        self.assertEqual(bin_obj.item_code, "ITEM-100")
        self.assertEqual(bin_obj.warehouse, "WH")
        self.assertEqual(bin_obj.actual_qty, 120)

    def test_to_inventory_bin_with_invalid_type(self):
        bin_obj = InventoryService._to_inventory_bin("invalid")
        self.assertIsNone(bin_obj)

    def test_to_inventory_bin_missing_required_fields(self):
        raw = {"item_code": "ITEM-200"}  # missing warehouse
        bin_obj = InventoryService._to_inventory_bin(raw)
        self.assertIsNone(bin_obj)

    # ---------- limit & continue coverage ----------

    def test_get_inventory_issues_respects_limit(self):
        bins = [
            InventoryBin("A", "WH", 300),
            InventoryBin("B", "WH", 250),
            InventoryBin("C", "WH", 150),
        ]

        issues = InventoryService.get_inventory_issues(bins, limit=1)

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].priority, "HIGH")

    def test_get_inventory_issues_skips_invalid_bin(self):
        bins = [
            InventoryBin("A", "WH", 300),     # valid
            {"bad": "data"},                  # invalid → triggers continue
            InventoryBin("B", "WH", 150),     # valid
        ]

        issues = InventoryService.get_inventory_issues(bins)

        self.assertEqual(len(issues), 2)
        self.assertEqual(issues[0].priority, "HIGH")
        self.assertEqual(issues[1].priority, "MEDIUM")


if __name__ == "__main__":
    unittest.main()
