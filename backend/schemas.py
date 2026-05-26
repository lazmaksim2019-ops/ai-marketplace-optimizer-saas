from pydantic import BaseModel, HttpUrl


class AnalyzeRequest(BaseModel):
    image_url: str | None = None
    image_base64: str | None = None
    description: str


class AnalyzeResponse(BaseModel):
    seo_title: str
    seo_description: str
    infographics_triggers: list[str]
    marketing_tips: str


class ErrorResponse(BaseModel):
    detail: str
