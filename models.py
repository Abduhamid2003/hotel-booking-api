from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Hotel(Base):
    __tablename__ = "отели"

    id = Column(Integer, primary_key=True, index=True, name="ид")
    nazvanie = Column(String, index=True, name="название")
    mestopolozhenie = Column(String, name="местоположение")
    opisanie = Column(String, name="описание")
    url_izobrazheniya = Column(String, nullable=True, name="url_изображения")

    nomera = relationship("Room", back_populates="otel")

class Room(Base):
    __tablename__ = "номера"

    id = Column(Integer, primary_key=True, index=True, name="ид")
    nomer_komnaty = Column(String, index=True, name="номер_комнаты")
    tip = Column(String, name="тип")  # стандарт, люкс и т.д.
    tsena_za_noch = Column(Float, name="цена_за_ночь")
    vmestimost = Column(Integer, name="вместимость")
    udobstva = Column(String, nullable=True, name="удобства")
    id_otelya = Column(Integer, ForeignKey("отели.ид"), name="ид_отеля")

    otel = relationship("Hotel", back_populates="nomera")
    bronirovaniya = relationship("Booking", back_populates="nomer")

class User(Base):
    __tablename__ = "пользователи"

    id = Column(Integer, primary_key=True, index=True, name="ид")
    email = Column(String, unique=True, index=True)
    kheshirovanny_parol = Column(String, name="хэшированный_пароль")
    polnoe_imya = Column(String, name="полное_имя")
    telefon = Column(String, nullable=True, name="телефон")
    yavlyaetsya_adminom = Column(Boolean, default=False, name="является_админом")

    bronirovaniya = relationship("Booking", back_populates="polzovatel")

class Booking(Base):
    __tablename__ = "бронирования"

    id = Column(Integer, primary_key=True, index=True, name="ид")
    data_zaezda = Column(Date, name="дата_заезда")
    data_vyezda = Column(Date, name="дата_выезда")
    obshaya_stoimost = Column(Float, name="общая_стоимость")
    status = Column(String, default="подтверждено", name="статус")
    sozdano_v = Column(DateTime, default=datetime.utcnow, name="создано_в")

    id_polzovatelya = Column(Integer, ForeignKey("пользователи.ид"), name="ид_пользователя")
    id_nomera = Column(Integer, ForeignKey("номера.ид"), name="ид_номера")

    polzovatel = relationship("User", back_populates="bronirovaniya")
    nomer = relationship("Room", back_populates="bronirovaniya")