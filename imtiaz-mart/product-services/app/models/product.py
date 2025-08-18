from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

# Category model
class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=50)
    subcategories: List["Subcategory"] = Relationship(back_populates="category")

# Subcategory model
class Subcategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=50)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="subcategories")
    products: List["Product"] = Relationship(back_populates="subcategory")

# Brand model
class Brand(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=50)
    products: List["Product"] = Relationship(back_populates="brand")

# Tag model
class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=50)
    products: List["Product"] = Relationship(back_populates="tags", link_model="ProductTag")

# ProductTag junction table (many-to-many)
class ProductTag(SQLModel, table=True):
    product_id: Optional[int] = Field(default=None, foreign_key="product.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)

# ProductImage model (one-to-many)
class ProductImage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")
    image_url: str = Field(max_length=255)
    product: Optional["Product"] = Relationship(back_populates="images")

# Product model
class ProductBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None
    price: float = Field(gt=0)
    discount_percentage: Optional[float] = Field(default=None, ge=0, le=100)
    stock: int = Field(ge=0)
    sku: Optional[str] = Field(default=None, max_length=20)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    subcategory_id: Optional[int] = Field(default=None, foreign_key="subcategory.id")
    brand_id: Optional[int] = Field(default=None, foreign_key="brand.id")
    weight: Optional[float] = Field(default=None, gt=0)
    dimensions: Optional[str] = Field(default=None, max_length=50)
    is_active: bool = Field(default=True)
    seo_title: Optional[str] = Field(default=None, max_length=70)
    seo_description: Optional[str] = Field(default=None, max_length=160)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: Optional[Category] = Relationship(back_populates="products")
    subcategory: Optional[Subcategory] = Relationship(back_populates="products")
    brand: Optional[Brand] = Relationship(back_populates="products")
    tags: List[Tag] = Relationship(back_populates="products", link_model=ProductTag)
    images: List[ProductImage] = Relationship(back_populates="product")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[float] = None
    discount_percentage: Optional[float] = None
    stock: Optional[int] = None
    sku: Optional[str] = None
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None
    brand_id: Optional[int] = None
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    is_active: Optional[bool] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None