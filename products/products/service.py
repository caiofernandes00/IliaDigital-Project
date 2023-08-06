import logging

from nameko.events import event_handler
from nameko.rpc import rpc

from products.dependencies import Storage, StorageWrapper
from products.schemas import Product

logger = logging.getLogger(__name__)


class ProductsService:

    name = 'products'

    storage: StorageWrapper = Storage()

    @rpc
    def get(self, product_id):
        product = self.storage.get(product_id)
        return Product().dump(product).data

    @rpc
    def list(self):
        products = self.storage.list()
        return Product(many=True).dump(products).data

    @rpc
    def create(self, product):
        product = Product(strict=True).load(product).data
        self.storage.create(product)

    @rpc
    def delete(self, product_id) -> None:
        self.storage.delete(product_id)

    @event_handler('orders', 'order_created')
    def handle_order_created(self, payload):
        for product in payload['order']['order_details']:
            self.storage.decrement_stock(
                product['product_id'], product['quantity'])
