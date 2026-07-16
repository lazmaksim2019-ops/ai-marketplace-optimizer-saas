from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient


class TestAnalyzeWithGemini:
    @patch("main._call_ai", new_callable=AsyncMock)
    def test_analyze_returns_valid_structure(
        self,
        mock_call_ai: AsyncMock,
        client: TestClient,
    ) -> None:
        mock_call_ai.return_value = {
            "seo_title": "Test title",
            "seo_description": "Test description",
            "infographics_triggers": ["Trigger 1", "Trigger 2"],
            "marketing_tips": "Test tip",
        }

        response = client.post(
            "/api/analyze",
            data={"description": "Тестовый товар", "marketplace": "wb"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "seo_title" in data
        assert "seo_description" in data
        assert "infographics_triggers" in data
        assert isinstance(data["infographics_triggers"], list)
        assert "marketing_tips" in data

    @patch("main._call_ai", new_callable=AsyncMock)
    def test_analyze_with_image_file(
        self,
        mock_call_ai: AsyncMock,
        client: TestClient,
        sample_image_bytes: bytes,
    ) -> None:
        mock_call_ai.return_value = {
            "seo_title": "Test",
            "seo_description": "Test",
            "infographics_triggers": [],
            "marketing_tips": "",
        }

        response = client.post(
            "/api/analyze",
            data={"description": "Товар с фото"},
            files={"file": ("test.jpg", sample_image_bytes, "image/jpeg")},
        )

        assert response.status_code == 200

    @patch("main._call_ai", new_callable=AsyncMock)
    def test_analyze_with_image_url(
        self,
        mock_call_ai: AsyncMock,
        client: TestClient,
    ) -> None:
        mock_call_ai.return_value = {
            "seo_title": "Test",
            "seo_description": "Test",
            "infographics_triggers": [],
            "marketing_tips": "",
        }

        response = client.post(
            "/api/analyze",
            data={
                "description": "Товар",
                "image_url": "https://example.com/image.jpg",
            },
        )

        assert response.status_code == 200

    @patch("main._call_ai", new_callable=AsyncMock)
    def test_ozon_marketplace_returns_data(
        self,
        mock_call_ai: AsyncMock,
        client: TestClient,
    ) -> None:
        mock_call_ai.return_value = {
            "seo_title": "Ozon title with keywords and benefits",
            "seo_description": "Marketing description for Ozon",
            "infographics_triggers": ["Бесплатная доставка", "Акция"],
            "marketing_tips": "Добавьте Rich-контент",
        }

        response = client.post(
            "/api/analyze",
            data={"description": "Товар для Ozon", "marketplace": "ozon"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["seo_title"]) > 10
