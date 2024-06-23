from dataclasses import dataclass
from model.product import product


@dataclass
class edges:
    product1: product
    product2: product
    weight: int
