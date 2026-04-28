from pydantic import BaseModel


class EventInput(BaseModel):
    type: int
    line: int
    lat: float
    lon: float
    moderated: int


class EventUpd(EventInput):
    id: str

class EventModel(BaseModel):
    id: str
    type: int
    line: int
    lat: float
    lon: float
    moderated: int
    my: bool
