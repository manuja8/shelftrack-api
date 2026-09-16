from fastapi import FastAPI, HTTPException

from app.service import get_item, list_items

app = FastAPI(
    title="ShelfTrack API",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "healthy", "application": "ShelfTrack API"}


@app.get("/items")
def items():
    return {"items": list_items()}


@app.get("/items/{sku}")
def item_by_sku(sku: str):
    item = get_item(sku)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
