from fastapi import FastAPI
from database import Base, engine
from routers import auth, hotels, rooms, bookings
from routers import download

app = FastAPI(
    title="Система бронирования отеля",
    description="API для управления отелями, номерами и бронированиями",
    version="1.0"
)

# Создаём таблицы в БД при запуске
Base.metadata.create_all(bind=engine)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(hotels.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(download.router)

@app.get("/")
def root():
    return {"message": "Добро пожаловать в API системы бронирования отеля!"}