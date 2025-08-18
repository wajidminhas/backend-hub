from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from datetime import datetime
from ..models.product import Product, ProductCreate, ProductUpdate, Category, Subcategory, Brand, Tag, ProductTag, ProductImage
from typing import List, Optional

async def create_product(product_data: ProductCreate, session: AsyncSession) -> Product:
    """Create a new product with related tags and images."""
    # Validate foreign keys
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
     # Create product
    db_product = Product(**product_data.model_dump(exclude={"image_urls", "tags"}))
    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)

    # Handle images
    if product_data.image_urls:
        for url in product_data.image_urls:
            db_image = ProductImage(product_id=db_product.id, image_url=str(url))
            session.add(db_image)

    # Handle tags
    if product_data.tags:
        for tag_name in product_data.tags:
            # Check if tag exists, create if not
            tag = (await session.exec(Tag.select().where(Tag.name == tag_name))).first()
            if not tag:
                tag = Tag(name=tag_name)
                session.add(tag)
                await session.commit()
                await session.refresh(tag)
            # Link tag to product
            product_tag = ProductTag(product_id=db_product.id, tag_id=tag.id)
            session.add(product_tag)

    await session.commit()
    await session.refresh(db_product)
    return db_product