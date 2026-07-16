from unittest.mock import AsyncMock

import httpx
import pytest
import respx

from marketplaces.base import RetryTransport
from marketplaces.ozon import OzonAPI
from marketplaces.schemas import UpdateCardRequest
from marketplaces.wb import WildberriesAPI


class TestWildberriesAPI:
    @pytest.fixture
    def api(self) -> WildberriesAPI:
        return WildberriesAPI(api_key="test-key", max_retries=1)

    @respx.mock
    async def test_get_products_success(self, api: WildberriesAPI) -> None:
        route = respx.post("https://content-api.wildberries.ru/content/v1/cards/cursor/list").mock(
            return_value=httpx.Response(
                200,
                json={
                    "data": {
                        "cards": [
                            {"nmID": 123, "title": "Test", "description": "Desc", "images": []},
                        ],
                    },
                },
            ),
        )

        result = await api.get_products()
        assert route.called
        assert result.total == 1
        assert result.products[0].external_id == "123"

    @respx.mock
    async def test_update_card_success(self, api: WildberriesAPI) -> None:
        route = respx.post("https://content-api.wildberries.ru/content/v1/cards/update").mock(
            return_value=httpx.Response(200, json={}),
        )

        result = await api.update_card(
            "123",
            UpdateCardRequest(
                seo_title="New title",
                seo_description="New desc",
                infographics_triggers=[],
            ),
        )
        assert route.called
        assert result.success is True

    @respx.mock
    async def test_update_card_failure(self, api: WildberriesAPI) -> None:
        respx.post("https://content-api.wildberries.ru/content/v1/cards/update").mock(
            return_value=httpx.Response(400, text="Bad Request"),
        )

        result = await api.update_card(
            "123",
            UpdateCardRequest(
                seo_title="T",
                seo_description="D",
                infographics_triggers=[],
            ),
        )
        assert result.success is False
        assert result.error is not None

    @respx.mock
    async def test_retry_on_429(self, api: WildberriesAPI) -> None:
        route = respx.post("https://content-api.wildberries.ru/content/v1/cards/cursor/list").mock(
            side_effect=[
                httpx.Response(429),
                httpx.Response(200, json={"data": {"cards": []}}),
            ],
        )

        result = await api.get_products()
        assert route.call_count == 2
        assert result.total == 0


class TestOzonAPI:
    @pytest.fixture
    def api(self) -> OzonAPI:
        return OzonAPI(api_key="ozon-key", client_id="123", max_retries=1)

    @respx.mock
    async def test_get_products_success(self, api: OzonAPI) -> None:
        route = respx.post("https://api-seller.ozon.ru/v1/product/list").mock(
            return_value=httpx.Response(
                200,
                json={
                    "result": {
                        "items": [
                            {"product_id": 456, "name": "Ozon Product", "description": "Desc"}
                        ],
                        "total": 1,
                    },
                },
            ),
        )

        result = await api.get_products()
        assert route.called
        assert result.total == 1
        assert result.products[0].external_id == "456"

    @respx.mock
    async def test_update_card_success(self, api: OzonAPI) -> None:
        route = respx.post("https://api-seller.ozon.ru/v1/product/import").mock(
            return_value=httpx.Response(200, json={}),
        )

        result = await api.update_card(
            "456",
            UpdateCardRequest(
                seo_title="Ozon title",
                seo_description="Ozon desc",
                infographics_triggers=[],
            ),
        )
        assert route.called
        assert result.success is True


class TestRetryTransport:
    @pytest.mark.parametrize("status", [429, 500, 502, 503])
    async def test_retries_on_server_error(self, status: int) -> None:
        mock_inner = AsyncMock(spec=httpx.AsyncBaseTransport)
        mock_inner.handle_async_request.side_effect = [
            httpx.Response(status, request=httpx.Request("GET", "http://test.com")),
            httpx.Response(200, request=httpx.Request("GET", "http://test.com")),
        ]

        transport = RetryTransport(inner=mock_inner, max_retries=2, base_delay=0.01)
        request = httpx.Request("GET", "http://test.com")
        response = await transport.handle_async_request(request)
        assert response.status_code == 200
        assert mock_inner.handle_async_request.call_count == 2

    async def test_gives_up_after_max_retries(self) -> None:
        mock_inner = AsyncMock(spec=httpx.AsyncBaseTransport)
        mock_inner.handle_async_request.return_value = httpx.Response(
            429,
            request=httpx.Request("GET", "http://test.com"),
        )

        transport = RetryTransport(inner=mock_inner, max_retries=2, base_delay=0.01)
        request = httpx.Request("GET", "http://test.com")
        response = await transport.handle_async_request(request)
        assert response.status_code == 429
        assert mock_inner.handle_async_request.call_count == 3
