from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from ..config.database import get_session, create_db_table

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/{product_id}")
async def get_product(product_id: int, session: AsyncSession = Depends(get_session)):
    # Example: Use session for database queries
    pass