import unittest
from app.models.inventory_models import InventoryBin, InventoryIssue


class TestInventoryModels(unittest.TestCase):

    def test_inventory_bin_defaults(self):
        bin_obj = InventoryBin(
            item_code="ITEM-1",
            warehouse="WH",
            actual_qty=10
        )

        # reserved_qty has default 0.0
        self.assertEqual(bin_obj.reserved_qty, 0.0)
        # stock_value default None
        self.assertIsNone(bin_obj.stock_value)

    def test_inventory_issue_to_dict(self):
        issue = InventoryIssue(
            item_code="ITEM-2",
            warehouse="Main WH",
            actual_qty=250,
            reserved_qty=5,
            priority="HIGH",
            reason="High quantity"
        )

        d = issue.to_dict()

        self.assertEqual(d["item_code"], "ITEM-2")
        self.assertEqual(d["warehouse"], "Main WH")
        self.assertEqual(d["actual_qty"], 250)
        self.assertEqual(d["reserved_qty"], 5)
        self.assertEqual(d["priority"], "HIGH")
        self.assertEqual(d["reason"], "High quantity")

        # optional: make sure keys are exactly as expected
        self.assertEqual(
            set(d.keys()),
            {"item_code", "warehouse", "actual_qty", "reserved_qty", "priority", "reason"}
        )


if __name__ == "__main__":
    unittest.main()
