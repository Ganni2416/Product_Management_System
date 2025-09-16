"""
batch_calc.py

Provides functionality to calculate total product stock in batches
using both threaded and asynchronous approaches.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from .models import Product

BATCH_SIZE = 10

def get_batches(products):
    return [products[i:i + BATCH_SIZE] for i in range(0, len(products), BATCH_SIZE)]

def calculate_batch_total(batch):
    return sum(p.qty for p in batch)

def batch_stock_total_threaded():
    products = Product.query.all()
    batches = get_batches(products)
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(calculate_batch_total, batches))
    return sum(results)

# Async version
async def calculate_batch_async(batch):
    await asyncio.sleep(0)  # simulate async operation
    return sum(p.qty for p in batch)

async def batch_stock_total_async():
    products = Product.query.all()
    batches = get_batches(products)
    tasks = [calculate_batch_async(batch) for batch in batches]
    results = await asyncio.gather(*tasks)
    return sum(results)
