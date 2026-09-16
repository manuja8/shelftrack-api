from fastapi.testclient import TestClient

from app.main import app
from app.service import stock_status


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_low_stock_business_rule():
    actual = stock_status(3)
    assert actual == "LOW_STOCK", (
        "automated test suite failure: expected LOW_STOCK "
        f"but received {actual}"
    )


def test_out_of_stock_business_rule():
    assert stock_status(0) == "OUT_OF_STOCK"


def test_get_known_item():
    response = client.get("/items/MS-200")
    assert response.status_code == 200
    assert response.json()["status"] == "LOW_STOCK"


def test_unknown_item_returns_404():
    response = client.get("/items/UNKNOWN")
    assert response.status_code == 404
