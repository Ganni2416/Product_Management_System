from flask import Blueprint, jsonify, request, abort
from .models import Product
from . import db
from .batch_calc import batch_stock_total_threaded, batch_stock_total_async
import asyncio

bp = Blueprint('routes', __name__, url_prefix='/api/products')


@bp.route("/", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


@bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())


@bp.route("/", methods=["POST"])
def create_product():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "qty", "price")):
        abort(400, "Missing product data")

    product = Product(name=data["name"], qty=data["qty"], price=data["price"])
    db.session.add(product)
    db.session.commit()

    return jsonify(product.to_dict()), 201


@bp.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    if not data:
        abort(400, "Missing update data")

    for field in ["name", "qty", "price"]:
        if field in data:
            setattr(product, field, data[field])
    db.session.commit()
    return jsonify(product.to_dict())


@bp.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return "", 204


@bp.route("/batch-stock/threaded", methods=["GET"])
def batch_stock_threaded():
    total = batch_stock_total_threaded()
    return jsonify({"batch_stock_total_threaded": total})


@bp.route("/batch-stock/async", methods=["GET"])
def batch_stock_async():
    total = asyncio.run(batch_stock_total_async())
    return jsonify({"batch_stock_total_async": total})

