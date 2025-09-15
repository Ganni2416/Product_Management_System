# app/crud.py
from .models import Product
from . import db

def create_product(name: str, qty: int, price: float) -> Product:
    product = Product(name=name, qty=qty, price=price)
    db.session.add(product)
    db.session.commit()
    return product

def get_product_by_id(product_id: int) -> Product:
    return Product.query.get(product_id)

def get_all_products() -> list:
    return Product.query.all()

def update_product(product_id: int, data: dict) -> Product:
    product = Product.query.get_or_404(product_id)
    for key in ["name", "qty", "price"]:
        if key in data:
            setattr(product, key, data[key])
    db.session.commit()
    return product

def delete_product(product_id: int) -> None:
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
