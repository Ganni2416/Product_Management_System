import pytest
from app import create_app, db
from app.models import Product
from app.batch_calc import batch_stock_total_threaded, batch_stock_total_async

@pytest.fixture
def app_with_products():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        for i in range(30):
            db.session.add(Product(name=f"Product {i+1}", qty=i+1, price=10.0))
        db.session.commit()
        yield app
        db.drop_all()

def test_batch_threaded_total(app_with_products):
    with app_with_products.app_context():
        total = batch_stock_total_threaded()
        assert total == sum(range(1, 31))  # Sum 1 to 30

@pytest.mark.asyncio
async def test_batch_async_total(app_with_products):
    with app_with_products.app_context():
        total = await batch_stock_total_async()
        assert total == sum(range(1, 31))  # Sum 1 to 30
