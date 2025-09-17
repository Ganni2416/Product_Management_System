# app/routes.py

from flask import Blueprint, jsonify, request, abort
from .models import Product
from . import db
from .batch_calc import batch_stock_total_threaded, batch_stock_total_async
from .emailer import send_email_async
import asyncio

bp = Blueprint('routes', __name__, url_prefix='/api/products')


@bp.route("/", methods=["GET"])
def get_products():
    """
    Get a list of all products.

    Returns:
        JSON list: A list of all products in JSON format.
    """
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


@bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """
    Get details of a single product by its ID.

    Args:
        product_id (int): The ID of the product to fetch.

    Returns:
        JSON object: The product data in JSON format.

    Raises:
        404 error if product is not found.
    """
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())


@bp.route("/", methods=["POST"])
def create_product():
    """
    Create a new product with provided JSON data.

    Expected JSON fields:
        - name (str): Product name.
        - qty (int): Quantity available.
        - price (float): Price of the product.

    Sends an email notification after successful creation.

    Returns:
        JSON object: The created product data.
        HTTP 201 status code on success.

    Raises:
        400 error if any required fields are missing.
    """
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "qty", "price")):
        abort(400, "Missing product data")

    product = Product(name=data["name"], qty=data["qty"], price=data["price"])
    db.session.add(product)
    db.session.commit()

    # Email notification on creation
    send_email_async(
        subject=f"✅ New Product Created: {product.name}",
        body=f"Product: {product.name}\nQuantity: {product.qty}\nPrice: ${product.price}",
        to="21eg505808@anurag.edu.in"
    )

    return jsonify(product.to_dict()), 201


@bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """
    Update an existing product's information by ID.

    Args:
        product_id (int): The ID of the product to update.

    Expected JSON fields (any subset):
        - name (str): New product name.
        - qty (int): New quantity.
        - price (float): New price.

    Sends an email notification after successful update.

    Returns:
        JSON object: The updated product data.

    Raises:
        400 error if update data is missing.
        404 error if product is not found.
    """
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    if not data:
        abort(400, "Missing update data")

    for field in ["name", "qty", "price"]:
        if field in data:
            setattr(product, field, data[field])
    db.session.commit()

    # Email notification on update
    send_email_async(
        subject=f"🔄 Product Updated: {product.name}",
        body=f"Updated Info:\nName: {product.name}\nQuantity: {product.qty}\nPrice: ${product.price}",
        to="21eg505808@anurag.edu.in"
    )

    return jsonify(product.to_dict())


@bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """
    Delete a product from the database by its ID.

    Args:
        product_id (int): The ID of the product to delete.

    Sends an email notification after successful deletion.

    Returns:
        Empty response with HTTP 204 status code on success.

    Raises:
        404 error if product is not found.
    """
    product = Product.query.get_or_404(product_id)
    product_name = product.name  # Save before deletion
    db.session.delete(product)
    db.session.commit()

    # Email notification on deletion
    send_email_async(
        subject=f"❌ Product Deleted: {product_name}",
        body=f"The product '{product_name}' was deleted from the system.",
        to="21eg505808@anurag.edu.in"
    )

    return "", 204


@bp.route("/batch-stock/threaded", methods=["GET"])
def batch_stock_threaded():
    """
    Calculate the total stock quantity using a threaded approach.

    Returns:
        JSON object: Contains total stock quantity calculated with threading.
        Example: {"batch_stock_total_threaded": 100}
    """
    total = batch_stock_total_threaded()
    return jsonify({"batch_stock_total_threaded": total})


@bp.route("/batch-stock/async", methods=["GET"])
def batch_stock_async():
    """
    Calculate the total stock quantity using an asynchronous approach.

    Returns:
        JSON object: Contains total stock quantity calculated asynchronously.
        Example: {"batch_stock_total_async": 100}
    """
    total = asyncio.run(batch_stock_total_async())
    return jsonify({"batch_stock_total_async": total})