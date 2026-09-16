LOW_STOCK_THRESHOLD = 5

ITEMS = {
    "KB-100": {"name": "Keyboard", "quantity": 12},
    "MS-200": {"name": "Mouse", "quantity": 3},
    "HD-300": {"name": "USB Hub", "quantity": 0},
}


def stock_status(quantity: int) -> str:
    if quantity <= 0:
        return "OUT_OF_STOCK"
    if quantity <= LOW_STOCK_THRESHOLD:
        return "LOW_STOCK"
    return "IN_STOCK"


def get_item(sku: str):
    item = ITEMS.get(sku)
    if item is None:
        return None

    return {
        "sku": sku,
        "name": item["name"],
        "quantity": item["quantity"],
        "status": stock_status(item["quantity"]),
    }


def list_items():
    return [get_item(sku) for sku in ITEMS]
