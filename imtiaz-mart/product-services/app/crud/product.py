from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException
from typing import List, Optional
from ..models.product import Product, ProductImage, ProductTag, Tag, Category
from ..schemas.product import ( 
    ProductCreate, ProductUpdate, ProductResponse,
    ProductImageCreate, ProductImageResponse,
    CategoryCreate, CategoryResponse,
    TagCreate, TagResponse
)
from ..models import Brand, Subcategory

from datetime import datetime

# Existing product-related CRUD functions
async def create_product(
    product_data: ProductCreate,
    session: AsyncSession
) -> Product:
    """Create a new product with related tags and images."""
    if product_data.category_id:
        category = await session.get(Category, product_data.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    if product_data.subcategory_id:
        subcategory = await session.get(Subcategory, product_data.subcategory_id)
        if not subcategory:
            raise HTTPException(status_code=404, detail="Subcategory not found")
        if subcategory.category_id != product_data.category_id:
            raise HTTPException(status_code=400, detail="Subcategory does not belong to the specified category")
    if product_data.brand_id:
        brand = await session.get(Brand, product_data.brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")

    db_product = Product(**product_data.dict(exclude={"image_urls", "tags"}))
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)

    if product_data.image_urls:
        for url in product_data.image_urls:
            db_image = ProductImage(product_id=db_product.id, image_url=str(url))
            session.add(db_image)

    if product_data.tags:
        for tag_name in product_data.tags:
            tag = (await session.exec(select(Tag).where(Tag.name == tag_name))).first()
            if not tag:
                tag = Tag(name=tag_name)
                session.add(tag)
                await session.commit()
                await session.refresh(tag)
            product_tag = ProductTag(product_id=db_product.id, tag_id=tag.id)
            session.add(product_tag)

    await session.commit()
    await session.refresh(db_product)
    return db_product

async def get_product(product_id: int, session: AsyncSession) -> Product:
    """Retrieve a product by ID."""
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    session: AsyncSession
) -> Product:
    """Update a product, including tags and images."""
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product_data.category_id:
        category = await session.get(Category, product_data.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    if product_data.subcategory_id:
        subcategory = await session.get(Subcategory, product_data.subcategory_id)
        if not subcategory:
            raise HTTPException(status_code=404, detail="Subcategory not found")
        if product_data.category_id and subcategory.category_id != product_data.category_id:
            raise HTTPException(status_code=400, detail="Subcategory does not belong to the specified category")
    if product_data.brand_id:
        brand = await session.get(Brand, product_data.brand_id)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")

    update_data = product_data.dict(exclude_unset=True, exclude={"image_urls", "tags"})
    update_data["updated_at"] = datetime.utcnow()
    for key, value in update_data.items():
        setattr(product, key, value)

    if product_data.image_urls is not None:
        await session.exec(ProductImage.delete().where(ProductImage.product_id == product_id))
        for url in product_data.image_urls or []:
            db_image = ProductImage(product_id=product_id, image_url=str(url))
            session.add(db_image)

    if product_data.tags is not None:
        await session.exec(ProductTag.delete().where(ProductTag.product_id == product_id))
        for tag_name in product_data.tags or []:
            tag = (await session.exec(select(Tag).where(Tag.name == tag_name))).first()
            if not tag:
                tag = Tag(name=tag_name)
                session.add(tag)
                await session.commit()
                await session.refresh(tag)
            product_tag = ProductTag(product_id=product_id, tag_id=tag.id)
            session.add(product_tag)

    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product

async def delete_product(product_id: int, session: AsyncSession) -> dict:
    """Delete a product and its related images and tags."""
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await session.exec(ProductImage.delete().where(ProductImage.product_id == product_id))
    await session.exec(ProductTag.delete().where(ProductTag.product_id == product_id))
    await session.delete(product)
    await session.commit()
    return {"message": "Product deleted"}

async def list_products(
    session: AsyncSession,
    category_id: Optional[int] = None,
    brand_id: Optional[int] = None,
    tag: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    is_active: Optional[bool] = True,
    limit: int = 20,
    offset: int = 0
) -> List[Product]:
    """Retrieve a paginated list of products with optional filters."""
    query = select(Product).where(Product.is_active == is_active)

    if category_id:
        query = query.where(Product.category_id == category_id)
    if brand_id:
        query = query.where(Product.brand_id == brand_id)
    if tag:
        query = query.join(ProductTag).join(Tag).where(Tag.name == tag)
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)

    query = query.offset(offset).limit(limit)
    result = await session.exec(query)
    return result.all()

async def search_products(
    session: AsyncSession,
    search_term: str,
    limit: int = 20,
    offset: int = 0
) -> List[Product]:
    """Search products by name, description, or SKU."""
    pattern = f"%{search_term}%"
    query = select(Product).where(
        (Product.name.ilike(pattern)) |
        (Product.description.ilike(pattern)) |
        (Product.sku.ilike(pattern))
    ).where(Product.is_active == True).offset(offset).limit(limit)

    result = await session.exec(query)
    return result.all()

async def bulk_update_products(
    session: AsyncSession,
    category_id: Optional[int] = None,
    brand_id: Optional[int] = None,
    discount_percentage: Optional[float] = None,
    is_active: Optional[bool] = None
) -> dict:
    """Update multiple products based on filters."""
    if discount_percentage is not None and (discount_percentage < 0 or discount_percentage > 100):
        raise HTTPException(status_code=400, detail="Discount must be between 0 and 100")

    query = select(Product)
    if category_id:
        query = query.where(Product.category_id == category_id)
    if brand_id:
        query = query.where(Product.brand_id == brand_id)

    products = (await session.exec(query)).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")

    for product in products:
        if discount_percentage is not None:
            product.discount_percentage = discount_percentage
        if is_active is not None:
            product.is_active = is_active
        product.updated_at = datetime.utcnow()
        session.add(product)

    await session.commit()
    return {"message": f"Updated {len(products)} products"}

async def add_product_image(
    session: AsyncSession,
    product_id: int,
    image_url: str
) -> ProductImage:
    """Add a single image to a product."""
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    image = ProductImage(product_id=product_id, image_url=image_url)
    session.add(image)
    await session.commit()
    await session.refresh(image)
    return image

async def delete_product_image(
    session: AsyncSession,
    product_id: int,
    image_id: int
) -> dict:
    """Delete a specific product image."""
    image = await session.get(ProductImage, image_id)
    if not image or image.product_id != product_id:
        raise HTTPException(status_code=404, detail="Image not found or not linked to product")

    await session.delete(image)
    await session.commit()
    return {"message": "Image deleted"}

# New category CRUD functions
async def create_category(
    category_data: CategoryCreate,
    session: AsyncSession
) -> Category:
    """Create a new category."""
    # Check if category name already exists
    existing = (await session.exec(select(Category).where(Category.name == category_data.name))).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category name already exists")

    db_category = Category(name=category_data.name)
    session.add(db_category)
    await session.commit()
    await session.refresh(db_category)
    return db_category

async def get_category(category_id: int, session: AsyncSession) -> Category:
    """Retrieve a category by ID."""
    category = await session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

async def list_categories(
    session: AsyncSession,
    limit: int = 20,
    offset: int = 0
) -> List[Category]:
    """List categories with pagination."""
    query = select(Category).offset(offset).limit(limit)
    result = await session.exec(query)
    return result.all()

# New tag CRUD functions
async def create_tag(
    tag_data: TagCreate,
    session: AsyncSession
) -> Tag:
    """Create a new tag."""
    existing = (await session.exec(select(Tag).where(Tag.name == tag_data.name))).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tag name already exists")

    db_tag = Tag(name=tag_data.name)
    session.add(db_tag)
    await session.commit()
    await session.refresh(db_tag)
    return db_tag

async def get_tag(tag_id: int, session: AsyncSession) -> Tag:
    """Retrieve a tag by ID."""
    tag = await session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

async def list_tags(
    session: AsyncSession,
    limit: int = 20,
    offset: int = 0
) -> List[Tag]:
    """List tags with pagination."""
    query = select(Tag).offset(offset).limit(limit)
    result = await session.exec(query)
    return result.all()