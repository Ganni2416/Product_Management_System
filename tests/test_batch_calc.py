# tests/test_batch_calc.py

import pytest
from app import create_app, db
from app.models import Product
from app.batch_calc import batch_stock_total_threaded, batch_stock_total_async
import asyncio

@pytest.fixture
def setup_products():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        # Add 30 products
        for i in range(30):
            db.session.add(Product(name=f"Product {i+1}", qty=i+1, price=10.0))
        db.session.commit()
        yield app
        db.drop_all()

def test_batch_threaded_total(setup_products):
    with setup_products.app_context():
        total = batch_stock_total_threaded()
        assert total == sum(range(1, 31))  # 1 to 30 sum

@pytest.mark.asyncio
async def test_batch_async_total(setup_products):
    with setup_products.app_context():
        total = await batch_stock_total_async()
        assert total == sum(range(1, 31))  # 1 to 30 sum
