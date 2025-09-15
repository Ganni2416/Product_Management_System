# tests/test_crud.py

import pytest
from app import create_app, db
from app.models import Product

@pytest.fixture
def test_app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(test_app):
    return test_app.test_client()

def test_create_product(client):
    res = client.post("/api/products/", json={"name": "Pen", "qty": 100, "price": 1.99})
    assert res.status_code == 201
    data = res.get_json()
    assert data["name"] == "Pen"
    assert data["qty"] == 100
    assert data["price"] == 1.99

def test_get_product(client):
    # Create first
    res = client.post("/api/products/", json={"name": "Pencil", "qty": 50, "price": 0.99})
    pid = res.get_json()["id"]
    
    # Then fetch
    res = client.get(f"/api/products/{pid}")
    assert res.status_code == 200
    data = res.get_json()
    assert data["name"] == "Pencil"
