"""Generates synthetic product records."""

import random
from datetime import datetime, timezone
from typing import List, Dict, Any

from config.settings import PRODUCTS_MIN, PRODUCTS_MAX, PRODUCT_CATEGORIES


def generate(batch_id: str) -> List[Dict[str, Any]]:
    """Generate 5–10 product documents."""
    count = random.randint(PRODUCTS_MIN, PRODUCTS_MAX)
    products: List[Dict[str, Any]] = []

    for _ in range(count):
        category = random.choice(list(PRODUCT_CATEGORIES.keys()))
        products.append(
            {
                "product_id": f"PROD{random.randint(1000, 99999)}",
                "product_name": random.choice(PRODUCT_CATEGORIES[category]),
                "category": category,
                "price": round(random.uniform(50, 15000), 2),
                "batch_id": batch_id,
                "created_at": datetime.now(timezone.utc),
            }
        )

    return products