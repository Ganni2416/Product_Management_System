from .models import Product
from . import db

def create_product(name: str, qty: int, price: float) -> Product:
    """
    Create and save a new product in the database.

    Args:
        name (str): Name of the product.
        qty (int): Quantity of the product.
        price (float): Price of the product.

    Returns:
        Product: The created Product object.
    """
    product = Product(name=name, qty=qty, price=price)
    db.session.add(product)
    db.session.commit()
    return product

def get_product_by_id(product_id: int) -> Product:
    """
    Retrieve a product by its ID.

    Args:
        product_id (int): The ID of the product to retrieve.

    Returns:
        Product or None: The Product object if found, else None.
    """
    return Product.query.get(product_id)

def get_all_products() -> list:
    """
    Retrieve all products from the database.

    Returns:
        list: List of all Product objects.
    """
    return Product.query.all()

def update_product(product_id: int, data: dict) -> Product:
    """
    Update a product's details by its ID.

    Args:
        product_id (int): The ID of the product to update.
        data (dict): Dictionary containing the fields to update 
                     (e.g., 'name', 'qty', 'price').

    Returns:
        Product: The updated Product object.

    Raises:
        404 error if the product with the given ID is not found.
    """
    product = Product.query.get_or_404(product_id)
    for key in ["name", "qty", "price"]:
        if key in data:
            setattr(product, key, data[key])
    db.session.commit()
    return product

def delete_product(product_id: int) -> None:
    """
    Delete a product from the database by its ID.

    Args:
        product_id (int): The ID of the product to delete.

    Raises:
        404 error if the product with the given ID is not found.
    """
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()

def save_products(products_list: list) -> None:
    """
    Save or update multiple products in the database.

    For each product in the list, checks if a product with the same name
    exists. If it does, updates its price and quantity; otherwise, creates
    a new product record.

    Args:
        products_list (list): List of dictionaries, each containing product data
                              with keys 'name', 'price', and optional 'qty'.
    """
    for product_data in products_list:
        existing = Product.query.filter_by(name=product_data['name']).first()
        if existing:
            # Update existing product
            existing.price = product_data['price']
            existing.qty = product_data.get('qty', 10)
        else:
            # Create new product
            new_product = Product(
                name=product_data['name'],
                price=product_data['price'],
                qty=product_data.get('qty', 10)
            )
            db.session.add(new_product)
    db.session.commit()
