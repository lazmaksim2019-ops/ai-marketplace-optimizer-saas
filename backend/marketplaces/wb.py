import logging
from typing import Any

from .base import BaseMarketplaceClient
from .schemas import MarketplaceProduct, ProductListResponse, UpdateCardRequest, UpdateCardResponse

logger = logging.getLogger(__name__)

CONTENT_API = "https://content-api.wildberries.ru"
STATISTICS_API = "https://statistics-api.wildberries.ru"


class WildberriesAPI(BaseMarketplaceClient):
    BASE_URL = CONTENT_API

    def __init__(self, api_key: str | None = None, **kwargs: Any):
        super().__init__(api_key=api_key, **kwargs)

    def _build_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def get_products(self, limit: int = 100, _offset: int = 0) -> ProductListResponse:
        payload = {
            "sort": {"cursor": {"limit": limit}},
            "filter": {"withPhoto": -1},
        }
        response = await self._client.post(
            f"{CONTENT_API}/content/v1/cards/cursor/list",
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

        products = []
        for card in data.get("data", {}).get("cards", []):
            products.append(
                MarketplaceProduct(
                    external_id=str(card.get("nmID", "")),
                    title=card.get("title", ""),
                    description=card.get("description", ""),
                    images=[img.get("url", "") for img in card.get("images", [])],
                    marketplace="wb",
                )
            )

        return ProductListResponse(products=products, total=len(products))

    async def update_card(self, nm_id: str, data: UpdateCardRequest) -> UpdateCardResponse:
        payload = {
            "nmId": int(nm_id),
            "data": [
                {"key": "title", "value": data.seo_title},
                {"key": "description", "value": data.seo_description},
            ],
        }
        response = await self._client.post(
            f"{CONTENT_API}/content/v1/cards/update",
            json=payload,
        )
        if response.status_code != 200:
            return UpdateCardResponse(
                success=False,
                marketplace_id=nm_id,
                error=f"WB API error: {response.text}",
            )
        return UpdateCardResponse(success=True, marketplace_id=nm_id)
