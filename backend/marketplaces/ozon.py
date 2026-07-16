import logging
from typing import Any

from .base import BaseMarketplaceClient
from .schemas import MarketplaceProduct, ProductListResponse, UpdateCardRequest, UpdateCardResponse

logger = logging.getLogger(__name__)

API_BASE = "https://api-seller.ozon.ru"


class OzonAPI(BaseMarketplaceClient):
    BASE_URL = API_BASE

    def __init__(
        self,
        api_key: str | None = None,
        client_id: str | None = None,
        **kwargs: Any,
    ):
        self.client_id = client_id
        super().__init__(api_key=api_key, **kwargs)

    def _build_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["Api-Key"] = self.api_key
        if self.client_id:
            headers["Client-Id"] = self.client_id
        return headers

    async def get_products(self, limit: int = 100, offset: int = 0) -> ProductListResponse:
        payload = {
            "filter": {"visibility": "ALL"},
            "limit": limit,
            "offset": offset,
        }
        response = await self._client.post(
            f"{API_BASE}/v1/product/list",
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

        products = []
        for item in data.get("result", {}).get("items", []):
            products.append(MarketplaceProduct(
                external_id=str(item.get("product_id", "")),
                title=item.get("name", ""),
                description=item.get("description", ""),
                images=[],
                marketplace="ozon",
            ))

        return ProductListResponse(products=products, total=data.get("result", {}).get("total", 0))

    async def update_card(self, product_id: str, data: UpdateCardRequest) -> UpdateCardResponse:
        payload = {
            "product_id": int(product_id),
            "name": data.seo_title,
            "description": data.seo_description,
        }
        response = await self._client.post(
            f"{API_BASE}/v1/product/import",
            json=payload,
        )
        if response.status_code != 200:
            return UpdateCardResponse(
                success=False,
                marketplace_id=product_id,
                error=f"Ozon API error: {response.text}",
            )
        return UpdateCardResponse(success=True, marketplace_id=product_id)
