import asyncio
import logging
from abc import ABC, abstractmethod

import httpx

logger = logging.getLogger(__name__)


class RetryTransport(httpx.AsyncBaseTransport):
    def __init__(
        self,
        inner: httpx.AsyncBaseTransport,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 30.0,
        retryable_statuses: frozenset[int] | None = None,
    ):
        self._inner = inner
        self._max_retries = max_retries
        self._base_delay = base_delay
        self._max_delay = max_delay
        self._retryable_statuses = retryable_statuses or frozenset({429, 500, 502, 503, 504})

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        for attempt in range(self._max_retries + 1):
            response = await self._inner.handle_async_request(request)

            if response.status_code not in self._retryable_statuses or attempt == self._max_retries:
                return response

            delay = min(self._base_delay * (2 ** attempt), self._max_delay)
            logger.warning(
                "Retry %d/%d after %ds (status=%d, url=%s)",
                attempt + 1, self._max_retries, delay,
                response.status_code, request.url,
            )
            await asyncio.sleep(delay)

        return response  # unreachable, but satisfies the type checker


class BaseMarketplaceClient(ABC):
    BASE_URL: str

    def __init__(
        self,
        api_key: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        self.api_key = api_key
        transport = RetryTransport(
            inner=httpx.AsyncHTTPTransport(),
            max_retries=max_retries,
        )
        self._client = httpx.AsyncClient(
            transport=transport,
            timeout=httpx.Timeout(timeout, connect=10.0),
            headers=self._build_headers(),
        )

    @abstractmethod
    def _build_headers(self) -> dict[str, str]:
        ...

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "BaseMarketplaceClient":
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
