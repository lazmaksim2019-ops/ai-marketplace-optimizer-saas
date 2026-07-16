import json
import logging
from io import BytesIO

import httpx
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from google import genai
from google.genai import types
from PIL import Image
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from config import settings
from schemas import AnalyzeResponse, ErrorResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address, default_limits=[])

app = FastAPI(title="AI Оптимизатор карточек WB/OZON", version="1.0.0")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT_WB = """Ты — эксперт по SEO-оптимизации карточек товаров для Wildberries.
Проанализируй изображение товара и его описание. Верни СТРОГО только JSON без пояснений:

{
  "seo_title": "Заголовок до 60 символов, без спама и дублирования слов, строгий минимализм",
  "seo_description": "Оптимизированное описание до 3000 символов. Вплети популярные поисковые запросы и синонимы (например: свитер, джемпер, пуловер, кофта) органично в читаемый текст. Избегай спама ключей через запятую.",
  "infographics_triggers": ["Триггер 1 для обложки (макс 25 символов)", "Триггер 2", "Триггер 3"],
  "marketing_tips": "Советы по улучшению продаж на Wildberries"
}"""

SYSTEM_PROMPT_OZON = """Ты — эксперт по SEO-оптимизации карточек товаров для Ozon.
Проанализируй изображение товара и его описание. Верни СТРОГО только JSON без пояснений:

{
  "seo_title": "Длинное богатое наименование по формуле (Тип + Бренд + Особенности) до 200 символов",
  "seo_description": "Маркетинговое описание для покупателя до 3000 символов. Упор на выгоды, преимущества и коммерческие аргументы. Для SEO на Ozon важнее характеристики и Rich-контент, а не текст.",
  "infographics_triggers": ["Триггер 1 для обложки (макс 25 символов)", "Триггер 2", "Триггер 3"],
  "marketing_tips": "Советы по улучшению продаж на Ozon"
}"""


def _resize_to_under_4mb(data: bytes) -> bytes:
    image = Image.open(BytesIO(data))
    max_size = 3.5 * 1024 * 1024
    quality = 85
    while True:
        buf = BytesIO()
        image.save(buf, format="JPEG", quality=quality)
        out = buf.getvalue()
        if len(out) <= max_size or quality <= 10:
            return out
        quality -= 5


async def _call_ai(
    file_bytes: bytes | None,
    mime_type: str | None,
    image_url: str | None,
    description: str,
    marketplace: str,
) -> AnalyzeResponse:
    if not settings.gemini_api_key or settings.gemini_api_key == "your_gemini_api_key_here":
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY не настроен. Добавьте ключ в файл .env",
        )

    http_options = None
    if settings.proxy_url:
        proxy_client = httpx.AsyncClient(proxy=settings.proxy_url)
        http_options = types.HttpOptions(httpx_async_client=proxy_client)

    system_prompt = SYSTEM_PROMPT_WB if marketplace == "wb" else SYSTEM_PROMPT_OZON

    client = genai.Client(
        api_key=settings.gemini_api_key,
        http_options=http_options,
    )

    prompt_text = f"Проанализируй этот товар. Текущее описание: {description}. Верни JSON."

    contents: list = [prompt_text]

    if file_bytes:
        resized = _resize_to_under_4mb(file_bytes)
        image_part = types.Part.from_bytes(data=resized, mime_type=mime_type or "image/jpeg")
        contents.insert(0, image_part)
    elif image_url and image_url.strip() and "example.com" not in image_url:
        contents.insert(0, image_url)

    try:
        response = await client.aio.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                temperature=0.7,
            ),
        )
    except Exception as e:
        err_str = str(e).lower()
        if "429" in err_str or "too many requests" in err_str or "resource exhausted" in err_str:
            logger.warning("Gemma API rate limit exceeded")
            raise HTTPException(
                status_code=429,
                detail="Лимит бесплатного API исчерпан. Подождите 60 секунд и повторите попытку.",
            )
        raise

    raw = json.loads(response.text)
    return AnalyzeResponse(**raw)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post(
    "/api/analyze",
    response_model=AnalyzeResponse,
    responses={400: {"model": ErrorResponse}, 429: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
@limiter.limit("10/minute")
async def analyze(
    request: Request,
    image_url: str | None = Form(None),
    file: UploadFile | None = File(None),
    description: str = Form(...),
    marketplace: str = Form("wb"),
):
    if marketplace not in ("wb", "ozon"):
        raise HTTPException(status_code=422, detail="marketplace must be 'wb' or 'ozon'")
    try:
        file_bytes: bytes | None = None
        mime_type: str | None = None

        if file and file.filename:
            file_bytes = await file.read()
            mime_type = file.content_type or "image/jpeg"

        return await _call_ai(file_bytes, mime_type, image_url, description, marketplace)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Analysis failed")
        raise HTTPException(status_code=500, detail=f"Ошибка анализа: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
