from typing import List

from product.domain.product_bond import ProductBond
from product.domain.value_object.product_source import ProductSource
from product.domain.value_object.timestamp import Timestamp


class ProductBondData:
    def __init__(self, items: List[ProductBond], source: ProductSource, fetched_at: Timestamp):
        self.items = items
        self.source = source
        self.fetched_at = fetched_at

    def add_item(self, item: ProductBond):
        self.items.append(item)