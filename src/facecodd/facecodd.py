from datetime import datetime

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import db_async_client
from src.models.logistic import Route
from src.schemas.token import Token

codd_router = APIRouter(prefix="/codd", tags=["CODD"])


@codd_router.get("/transport")
async def transport(route_id: int, session: AsyncSession = db_async_client):
    route = await session.get(Route, route_id)
    real_time = datetime.now()
    real_time = d
    lat = 3.14
    lon = 2.71
    data = [
        lat,
        lon,
        route.number,
        real_time.isoformat()
    ]
    return data

