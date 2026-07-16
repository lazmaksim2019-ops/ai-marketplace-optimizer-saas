from pydantic import BaseModel


class MarketplaceProduct(BaseModel):
    external_id: str
    title: str
    description: str
    images: list[str]
    marketplace: str


class ProductListResponse(BaseModel):
    products: list[MarketplaceProduct]
    total: int


class UpdateCardRequest(BaseModel):
    seo_title: str
    seo_description: str
    infographics_triggers: list[str]


class UpdateCardResponse(BaseModel):
    success: bool
    marketplace_id: str | None = None
    error: str | None = None
