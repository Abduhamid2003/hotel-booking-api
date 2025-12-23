from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Booking, Room, User
from schemas import BookingCreate, BookingResponse
from dependencies import get_current_user
from datetime import date

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

# Проверка доступности номера на даты
def is_room_available(db: Session, room_id: int, check_in: date, check_out: date):
    conflicting = db.query(Booking).filter(
        Booking.id_nomera == room_id,  # исправлено с room_id на id_nomera
        Booking.status != "отменено",
        Booking.data_zaezda < check_out,  # исправлено с check_in_date
        Booking.data_vyezda > check_in    # исправлено с check_out_date
    ).first()
    return conflicting is None

@router.post("/", response_model=BookingResponse)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Создать новое бронирование
    """
    if booking.data_zaezda >= booking.data_vyezda:
        raise HTTPException(status_code=400, detail="Дата выезда должна быть позже даты заезда")

    room = db.query(Room).filter(Room.id == booking.id_nomera).first()
    if not room:
        raise HTTPException(status_code=404, detail="Номер не найден")

    if not is_room_available(db, booking.id_nomera, booking.data_zaezda, booking.data_vyezda):
        raise HTTPException(status_code=400, detail="Номер уже забронирован на выбранные даты")

    dni = (booking.data_vyezda - booking.data_zaezda).days
    obshaya_stoimost = dni * room.tsena_za_noch

    new_booking = Booking(
        **booking.dict(),
        id_polzovatelya=current_user.id,
        obshaya_stoimost=obshaya_stoimost
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("/", response_model=list[BookingResponse])
def get_my_bookings(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Получить все бронирования текущего пользователя
    """
    return db.query(Booking).filter(Booking.id_polzovatelya == current_user.id).all()

@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    """
    Отменить бронирование
    """
    booking = db.query(Booking).filter(
        Booking.id == booking_id, 
        Booking.id_polzovatelya == current_user.id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Бронирование не найдено")
    booking.status = "отменено"
    db.commit()
    return {"detail": "Бронирование отменено"}