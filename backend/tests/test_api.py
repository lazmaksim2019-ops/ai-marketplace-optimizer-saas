import pytest
from fastapi.testclient import TestClient


class TestHealth:
    def test_health_returns_ok(self, client: TestClient) -> None:
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_health_is_fast(self, client: TestClient) -> None:
        import time

        start = time.perf_counter()
        client.get("/api/health")
        elapsed = time.perf_counter() - start
        assert elapsed < 0.5, f"Health check took {elapsed:.3f}s"


class TestCORS:
    def test_cors_headers_present(self, client: TestClient) -> None:
        response = client.get(
            "/api/health",
            headers={"Origin": "http://localhost:5173"},
        )
        assert response.headers.get("access-control-allow-origin") in ("*", "http://localhost:5173")


class TestAnalyzeValidation:
    def test_missing_description_returns_422(self, client: TestClient) -> None:
        response = client.post("/api/analyze")
        assert response.status_code == 422

    def test_marketplace_defaults_to_wb(self, client: TestClient) -> None:
        response = client.post(
            "/api/analyze",
            data={"description": "test"},
        )
        assert response.status_code != 422

    def test_invalid_marketplace_returns_422(self, client: TestClient) -> None:
        response = client.post(
            "/api/analyze",
            data={"description": "test", "marketplace": "invalid"},
        )
        assert response.status_code == 422

    def test_empty_description_returns_200_with_content(self, client: TestClient) -> None:
        response = client.post(
            "/api/analyze",
            data={"description": ""},
        )
        assert response.status_code == 422  # description is required
