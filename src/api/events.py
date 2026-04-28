from typing import Optional, List
import hashlib
import json

from fastapi import APIRouter, Header, Response, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import db_async_client
from src.schemas.event import EventModel
from src.schemas.eventwrited import EventWrited
from src.services.events import EventsService

events_router = APIRouter(
    prefix="/events",
    tags=["Дорожные события"],
)


@events_router.post("/write")
async def create_event(data: EventWrited, token: str = Header(...), session: AsyncSession = db_async_client):
    """
    Записывает в базу данных новый пользовательский отзыв
    :param data: содержание отзыва
    :param token: Авторизационный токен пользователя
    :param session: Сессия БД
    :return: Сообщение
    """
    event = await EventsService.write_event(session, token, data)
    return event


@events_router.get(
    "/all",
    response_model=List[EventModel],
    responses={status.HTTP_304_NOT_MODIFIED: {"description": "Не изменилось"}},
)
async def get_all_events(
    token: Optional[str] = Header(None),
    if_none_match: Optional[str] = Header(None),
    session: AsyncSession = db_async_client,
):
    """
    Передает список всех дорожных событий
    :param token: Авторизационный токен пользователя
    :param if_none_match: ETag текущей версии данных на клиенте
    :param session: Сессия БД
    :return: Список моделей дорожных событий или 304, если данные не изменились
    """
    events = await EventsService.get_all_events(session, token)

    events_json = json.dumps(jsonable_encoder(events), sort_keys=True, ensure_ascii=False)
    etag = hashlib.md5(events_json.encode("utf-8")).hexdigest()

    if if_none_match == etag:
        return Response(
            status_code=status.HTTP_304_NOT_MODIFIED,
            headers={"ETag": etag},
        )

    return Response(
        content=events_json,
        media_type="application/json",
        headers={"ETag": etag},
    )


@events_router.delete("/clear")
async def delete_event(event_id: str, token: str = Header(...), session: AsyncSession = db_async_client):
    """
    Удаляет остановку из избранного
    :param stop_id: айди остановки
    :param token: Авторизационный токен пользователя
    :param session: Сессия БД
    :return: Модель обновленной остановки
    """
    event = await EventsService.clear_event(session, token, event_id)
    return event


@events_router.patch("/fix")
async def fix_event(event_id: str, token: str = Header(...), session: AsyncSession = db_async_client):
    """
    Удаляет остановку из избранного
    :param stop_id: айди остановки
    :param token: Авторизационный токен пользователя
    :param session: Сессия БД
    :return: Модель обновленной остановки
    """
    event = await EventsService.fix_event(session, token, event_id)
    return event