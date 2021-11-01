import json

from faire_api_client.utils import urljoin

class ResourcePool:
    def __init__(self, endpoint, session):
        """Initialize the ResourcePool to the given endpoint. Eg: products"""
        self._endpoint = endpoint
        self._session = session

    def get_url(self):
        return self._endpoint

class CreatableResource:
    def create_item(self, item, files=None):
        if files:
            self._session.headers.pop('Content-Type')
            self._session.headers.pop('Accept')
            res = self._session.post(self._endpoint, files=files, data=item)
        else:
            res = self._session.post(self._endpoint, data=json.dumps(item))
        return res

class GettableResource:
    def fetch_item(self, code):
        url = urljoin(self._endpoint, code)
        res = self._session.get(url)
        return res

class ListableResource:
    def fetch_list(self, args=None):
        res = self._session.get(self._endpoint, params=args)
        return res

class SearchableResource:
    def search(self, query):
        params = {
            'query': query
        }
        res = self._session.get(self._endpoint, params=params)
        return res

class UpdatableResource:
    def update_create_item(self, item, code=None):
        url = urljoin(self._endpoint, code) if code else self._endpoint
        res = self._session.put(url, data=json.dumps(item))
        return res

    def update_item(self, item, code=None):
        url = urljoin(self._endpoint, code) if code else self._endpoint
        res = self._session.patch(url, data=json.dumps(item))
        return res        

class DeletableResource:
    def delete_item(self, code):
        url = urljoin(self._endpoint, code)
        res = self._session.delete(url)
        return res

# Pools

# Orders
class OrdersProcessingPool(ResourcePool, UpdatableResource):
    pass

class OrdersShipmentsPool(ResourcePool, CreatableResource):
    pass

class OrdersItemsAvailabilityPool(ResourcePool, CreatableResource):
    pass

class OrdersItemsPool(ResourcePool):

    @property
    def availability(self):
        return OrdersItemsAvailabilityPool(
            urljoin(self._endpoint, 'availability'), self._session
        )

class OrdersPool(
    ResourcePool, 
    ListableResource,
    GettableResource):
    
    def processing(self, order_id):
        return OrdersProcessingPool(
            urljoin(self._endpoint, order_id, 'processing'), self._session
        )

    def shipments(self, order_id):
        return OrdersShipmentsPool(
            urljoin(self._endpoint, order_id, 'shipments'), self._session
        )

    def items(self, order_id):
        return OrdersItemsPool(
            urljoin(self._endpoint, order_id, 'items'), self._session
        )

# Products
class ProductsVariantOptionSetsPool(ResourcePool, UpdatableResource):
    pass

class ProductsTypesPool(ResourcePool, ListableResource):
    pass

class ProductsVariantsPool(ResourcePool, CreatableResource, UpdatableResource, DeletableResource):
    pass

class ProductsVariantsInventoryLevelsPool(ResourcePool, UpdatableResource):
    pass

class ProductsVariantsInventoryPool(ResourcePool):
    @property
    def inventory_levels_by_product_variant_ids(self):
        return ProductsVariantsInventoryLevelsPool(
            urljoin(self._endpoint, 'inventory-levels-by-product-variant-ids'), self._session
        )

    @property
    def inventory_levels_by_skus(self):
        return ProductsVariantsInventoryLevelsPool(
            urljoin(self._endpoint, 'inventory-levels-by-skus'), self._session
        )

class ProductsPrepacksPool(ResourcePool, CreatableResource, GettableResource, ListableResource, DeletableResource):
    pass

class ProductsPool(ResourcePool, ListableResource, GettableResource, CreatableResource, UpdatableResource, DeletableResource):
    
    @property
    def types(self):
        return ProductsTypesPool(
            urljoin(self._endpoint, 'types'), self._session
        )

    @property
    def variants_inventory(self):
        return ProductsVariantsInventoryPool(
            urljoin(self._endpoint, 'variants'), self._session
        )

    def prepacks(self, product_id):
        return ProductsPrepacksPool(
            urljoin(self._endpoint, product_id, 'prepacks'), self._session
        )

    def variant_option_sets(self, product_id):
        return ProductsVariantOptionSetsPool(
            urljoin(self._endpoint, product_id, 'variant-option-sets'), self._session
        )

    def variants(self, products_id):
        return ProductsVariantsPool(
            urljoin(self._endpoint, products_id, 'variants'), self._session
        )

# Brands
class BrandsProfilePool(ResourcePool, ListableResource):
    pass

class BrandsPool(ResourcePool):
    
    @property
    def profile(self):
        return BrandsProfilePool(
            urljoin(self._endpoint, 'profile'), self._session
        )

# Retailers
class RetailersPublicPool(ResourcePool, GettableResource):
    pass

class RetailersPool(ResourcePool):
    
    @property
    def public(self):
        return RetailersPublicPool(
            urljoin(self._endpoint, 'public'), self._endpoint
        )