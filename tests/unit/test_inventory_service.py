from app.models.inventory_models import InventoryBin
from app.services.inventory_service import InventoryService


def test_high_priority_inventory():
    bin = InventoryBin(
        item_code="ITEM-001",
        warehouse="Main Warehouse",
        actual_qty=250,
        reserved_qty=0
    )

    issue = InventoryService.calculate_priority(bin)

    assert issue is not None
    assert issue.priority == "HIGH"
    assert "quantity" in issue.reason.lower()


def test_medium_priority_inventory():
    bin = InventoryBin(
        item_code="ITEM-002",
        warehouse="Main Warehouse",
        actual_qty=150,
        reserved_qty=0
    )

    issue = InventoryService.calculate_priority(bin)

    assert issue is not None
    assert issue.priority == "MEDIUM"


def test_low_priority_inventory():
    bin = InventoryBin(
        item_code="ITEM-003",
        warehouse="Main Warehouse",
        actual_qty=50,
        reserved_qty=0
    )

    issue = InventoryService.calculate_priority(bin)

    assert issue is not None
    assert issue.priority == "LOW"


def test_inventory_issues_sorted_by_priority():
    bins = [
        InventoryBin("A", "WH", 50),
        InventoryBin("B", "WH", 300),
        InventoryBin("C", "WH", 150),
    ]

    issues = InventoryService.get_inventory_issues(bins)

    assert issues[0].priority == "HIGH"
    assert issues[1].priority == "MEDIUM"
    assert issues[2].priority == "LOW"
