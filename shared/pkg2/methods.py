from pkg1.types import InventoryItem

def swap_prices(a: InventoryItem, b: InventoryItem):
    temp = b.unit_price
    b.unit_price = a.unit_price
    a.unit_price = temp