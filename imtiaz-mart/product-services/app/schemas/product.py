from pydantic import BaseModel, PositiveFloat, NonNegativeInt, HttpUrl, field_validator
from typing import Optional, List
from datetime import datetime
import re

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: PositiveFloat
    discount_percentage: Optional[PositiveFloat] = None
    stock: NonNegativeInt
    sku: Optional[str] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    brand_id: Optional[int] = None
    weight: Optional[PositiveFloat] = None
    dimensions: Optional[str] = None
    is_active: bool = True
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Product name cannot be empty")
        if len(value) > 100:
            raise ValueError("Product name must be 100 characters or less")
        return value.strip()

    @field_validator("sku")
    @classmethod
    def validate_sku(cls, value: Optional[str]) -> Optional[str]:
        if value:
            if not re.match(r"^[a-zA-Z0-9]{3,20}$", value):
                raise ValueError("SKU must be alphanumeric and 3-20 characters")
        return value

    @field_validator("discount_percentage")
    @classmethod
    def validate_discount(cls, value: Optional[float]) -> Optional[float]:
        if value is not None and (value < 0 or value > 100):
            raise ValueError("Discount percentage must be between 0 and 100")
        return value

    @field_validator("dimensions")
    @classmethod
    def validate_dimensions(cls, value: Optional[str]) -> Optional[str]:
        if value:
            if not re.match(r"^\d+(\.\d+)?x\d+(\.\d+)?x\d+(\.\d+)?\s*(cm|m|in|ft)$", value):
                raise ValueError("Dimensions must be in format 'LxWxH unit' (e.g., '10x5x2 cm')")
        return value

    @field_validator("seo_title")
    @classmethod
    def validate_seo_title(cls, value: Optional[str]) -> Optional[str]:
        if value and len(value) > 70:
            raise ValueError("SEO title must be 70 characters or less")
        return value

    @field_validator("seo_description")
    @classmethod
    def validate_seo_description(cls, value: Optional[str]) -> Optional[str]:
        if value and len(value) > 160:
            raise ValueError("SEO description must be 160 characters or less")
        return value

class ProductCreate(ProductBase):
    image_urls: Optional[List[HttpUrl]] = None
    tags: Optional[List[str]] = None

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[PositiveFloat] = None
    discount_percentage: Optional[PositiveFloat] = None
    stock: Optional[NonNegativeInt] = None
    sku: Optional[str] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    brand_id: Optional[int] = None
    weight: Optional[PositiveFloat] = None
    dimensions: Optional[str] = None
    is_active: Optional[bool] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    image_urls: Optional[List[HttpUrl]] = None
    tags: Optional[List[str]] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    category_name: Optional[str] = None
    subcategory_name: Optional[str] = None
    brand_name: Optional[str] = None
    image_urls: Optional[List[str]] = None
    tags: Optional[List[str]] = None

    model_config = {"from_attributes": True}