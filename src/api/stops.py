from typing import List, Optional
import hashlib
import json

from fastapi import APIRouter, Header, Response, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import db_async_client
from src.schemas.stop import StopModel
from src.services.stops import StopService

stops_router = APIRouter(
    prefix="/stops",
    tags=["Остановки"],
)


@stops_router.get(
    "/all",
    response_model=List[StopModel],
    responses={status.HTTP_304_NOT_MODIFIED: {"description": "Не изменилось"}},
)
async def get_all_stops(
    token: Optional[str] = Header(None),
    if_none_match: Optional[str] = Header(None),
    session: AsyncSession = db_async_client,
):
    """
    Передает список всех остановок города
    :param token: Авторизационный токен пользователя
    :param if_none_match: ETag текущей версии данных на клиенте
    :param session: Сессия БД
    :return: Список моделей остановок или 304, если данные не изменились
    """
    stops = await StopService.get_all_stops(session, token)

    stops_json = json.dumps(jsonable_encoder(stops), sort_keys=True, ensure_ascii=False)
    etag = hashlib.md5(stops_json.encode("utf-8")).hexdigest()

    if if_none_match == etag:
        return Response(
            status_code=status.HTTP_304_NOT_MODIFIED,
            headers={"ETag": etag},
        )

    return Response(
        content=stops_json,
        media_type="application/json",
        headers={"ETag": etag},
    )


@stops_router.post("/like", response_model=StopModel)
async def like_stop(stop_id: int, token: str = Header(...), session: AsyncSession = db_async_client):
    """
    Добавляет остановку в избранное
    :param stop_id: айди остановки
    :param token: Авторизационный токен пользователя
    :param session: Сессия БД
    :return: Модель обновленной остановки
    """
    stop = await StopService.like_stop(session, token, stop_id)
    return stop


@stops_router.delete("/dislike", response_model=StopModel)
async def like_stop(stop_id: int, token: str = Header(...), session: AsyncSession = db_async_client):
    """
    Удаляет остановку из избранного
    :param stop_id: айди остановки
    :param token: Авторизационный токен пользователя
    :param session: Сессия БД
    :return: Модель обновленной остановки
    """
    stop = await StopService.dislike_stop(session, token, stop_id)
    return stop
