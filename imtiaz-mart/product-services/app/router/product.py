from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from ..config.database import get_session
from ..crud.product import (
    create_product, get_product, update_product, delete_product,
    list_products, search_products, bulk_update_products,
    add_product_image, delete_product_image,
    create_category, get_category, list_categories,
    create_tag, get_tag, list_tags
)
from ..schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse,
    ProductImageCreate, ProductImageResponse,
    CategoryCreate, CategoryResponse,
    TagCreate, TagResponse
)

router = APIRouter(prefix="/products", tags=["products"])

# Product routes
@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product_endpoint(
    product: ProductCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create a new product."""
    try:
        return await create_product(product, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create product: {str(e)}")

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_endpoint(
    product_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Retrieve a product by ID."""
    return await get_product(product_id, session)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product_endpoint(
    product_id: int,
    product: ProductUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Update a product by ID."""
    try:
        return await update_product(product_id, product, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update product: {str(e)}")

@router.delete("/{product_id}", status_code=200)
async def delete_product_endpoint(
    product_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Delete a product by ID."""
    return await delete_product(product_id, session)

@router.get("/", response_model=List[ProductResponse])
async def list_products_endpoint(
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    brand_id: Optional[int] = Query(None, description="Filter by brand ID"),
    tag: Optional[str] = Query(None, description="Filter by tag name"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    is_active: Optional[bool] = Query(True, description="Filter by active status"),
    limit: int = Query(20, ge=1, le=100, description="Number of products to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    session: AsyncSession = Depends(get_session)
):
    """List products with optional filters and pagination."""
    return await list_products(
        session, category_id, brand_id, tag, min_price, max_price, is_active, limit, offset
    )

@router.get("/search", response_model=List[ProductResponse])
async def search_products_endpoint(
    q: str = Query(..., description="Search term for name, description, or SKU"),
    limit: int = Query(20, ge=1, le=100, description="Number of products to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    session: AsyncSession = Depends(get_session)
):
    """Search products by name, description, or SKU."""
    return await search_products(session, q, limit, offset)

@router.patch("/bulk", status_code=200)
async def bulk_update_products_endpoint(
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    brand_id: Optional[int] = Query(None, description="Filter by brand ID"),
    discount_percentage: Optional[float] = Query(None, ge=0, le=100, description="Set discount percentage"),
    is_active: Optional[bool] = Query(None, description="Set active status"),
    session: AsyncSession = Depends(get_session)
):
    """Bulk update products based on filters."""
    try:
        return await bulk_update_products(session, category_id, brand_id, discount_percentage, is_active)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to bulk update products: {str(e)}")

@router.post("/{product_id}/images", response_model=ProductImageResponse, status_code=201)
async def add_product_image_endpoint(
    product_id: int,
    image: ProductImageCreate,
    session: AsyncSession = Depends(get_session)
):
    """Add an image to a product."""
    try:
        return await add_product_image(session, product_id, image.image_url)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add image: {str(e)}")

@router.delete("/{product_id}/images/{image_id}", status_code=200)
async def delete_product_image_endpoint(
    product_id: int,
    image_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Delete a specific product image."""
    return await delete_product_image(session, product_id, image_id)

# Category routes
@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category_endpoint(
    category: CategoryCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create a new category."""
    try:
        return await create_category(category, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create category: {str(e)}")

@router.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category_endpoint(
    category_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Retrieve a category by ID."""
    return await get_category(category_id, session)

@router.get("/categories", response_model=List[CategoryResponse])
async def list_categories_endpoint(
    limit: int = Query(20, ge=1, le=100, description="Number of categories to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    session: AsyncSession = Depends(get_session)
):
    """List categories with pagination."""
    return await list_categories(session, limit, offset)

# Tag routes
@router.post("/tags", response_model=TagResponse, status_code=201)
async def create_tag_endpoint(
    tag: TagCreate,
    session: AsyncSession = Depends(get_session)
):
    """Create a new tag."""
    try:
        return await create_tag(tag, session)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create tag: {str(e)}")

@router.get("/tags/{tag_id}", response_model=TagResponse)
async def get_tag_endpoint(
    tag_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Retrieve a tag by ID."""
    return await get_tag(tag_id, session)

@router.get("/tags", response_model=List[TagResponse])
async def list_tags_endpoint(
    limit: int = Query(20, ge=1, le=100, description="Number of tags to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    session: AsyncSession = Depends(get_session)
):
    """List tags with pagination."""
    return await list_tags(session, limit, offset)