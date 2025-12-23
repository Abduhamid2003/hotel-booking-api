from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class HotelBase(BaseModel):
    nazvanie: str
    mestopolozhenie: str
    opisanie: Optional[str] = None
    url_izobrazheniya: Optional[str] = None

class HotelCreate(HotelBase):
    pass

class HotelResponse(HotelBase):
    id: int

    class Config:
        from_attributes = True

class RoomBase(BaseModel):
    nomer_komnaty: str
    tip: str
    tsena_za_noch: float
    vmestimost: int
    udobstva: Optional[str] = None
    id_otelya: int

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    parol: str
    polnoe_imya: str
    telefon: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    polnoe_imya: str
    yavlyaetsya_adminom: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class BookingCreate(BaseModel):
    data_zaezda: date
    data_vyezda: date
    id_nomera: int

class BookingResponse(BaseModel):
    id: int
    data_zaezda: date
    data_vyezda: date
    obshaya_stoimost: float
    status: str
    nomer: RoomResponse
    polzovatel: UserResponse

    class Config:
        from_attributes = True