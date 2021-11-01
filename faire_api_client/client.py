import requests as rq

from faire_api_client import (
    resources,
    utils
)
from faire_api_client.config import settings


class Client:
    def __init__(self, access_token, api_version=settings.API_VERSION):
        self._session = rq.Session()
        self._base_url = utils.urljoin(settings.BASE_URL, api_version)

        self._authenticate(access_token)

        self._resources = {
            'orders': resources.OrdersPool(
                utils.urljoin(self._base_url, 'orders'), self._session
            ),
            'products': resources.ProductsPool(
                utils.urljoin(self._base_url, 'products'), self._session
            ),
            'brands': resources.BrandsPool(
                utils.urljoin(self._base_url, 'brands'), self._session
            ),
            'retailers': resources.RetailersPool(
                utils.urljoin(self._base_url, 'retailers'), self._session
            ),
        }

    def _authenticate(self, access_token):
        
        self._session.headers.update({
            'X-FAIRE-ACCESS-TOKEN': access_token
        })

    @property
    def resources(self):
        return self._resources

    @property
    def orders(self):
        return self.resources['orders']

    @property
    def products(self):
        return self.resources['products']

    @property
    def brands(self):
        return self.resources['brands']

    @property
    def retailers(self):
        return self.resources['retailers']