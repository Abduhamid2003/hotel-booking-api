from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Hotel
from schemas import HotelCreate, HotelResponse
from dependencies import get_current_user
from models import User

router = APIRouter(prefix="/hotels", tags=["Отели"])

# Только админ может создавать/удалять отели
def get_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.yavlyaetsya_adminom:
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    return current_user

@router.post("/", response_model=HotelResponse)
def create_hotel(
    hotel: HotelCreate, 
    db: Session = Depends(get_db), 
    admin: User = Depends(get_admin_user)
):
    """
    Создать новый отель (только для администраторов)
    """
    db_hotel = Hotel(**hotel.dict())
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

@router.get("/", response_model=list[HotelResponse])
def get_hotels(db: Session = Depends(get_db)):
    """
    Получить список всех отелей
    """
    return db.query(Hotel).all()

@router.get("/{hotel_id}", response_model=HotelResponse)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    """
    Получить информацию об отеле по ID
    """
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Отель не найден")
    return hotel