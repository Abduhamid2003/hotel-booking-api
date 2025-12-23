from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Room, Hotel
from schemas import RoomCreate, RoomResponse
from dependencies import get_admin_user

router = APIRouter(prefix="/rooms", tags=["Номера"])

@router.post("/", response_model=RoomResponse)
def create_room(
    room: RoomCreate, 
    db: Session = Depends(get_db), 
    admin = Depends(get_admin_user)
):
    """
    Создать новый номер (только для администраторов)
    """
    # Проверка существования отеля
    if not db.query(Hotel).filter(Hotel.id == room.id_otelya).first():
        raise HTTPException(status_code=404, detail="Отель не найден")
    db_room = Room(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.get("/hotel/{hotel_id}", response_model=list[RoomResponse])
def get_rooms_by_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """
    Получить все номера определенного отеля
    """
    return db.query(Room).filter(Room.id_otelya == hotel_id).all()