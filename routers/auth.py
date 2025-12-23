from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, Token
from dependencies import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Аутентификация"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    
    hashed = get_password_hash(user.parol)
    new_user = User(
        email=user.email, 
        kheshirovanny_parol=hashed,  # исправлено
        polnoe_imya=user.polnoe_imya,  # исправлено
        telefon=user.telefon  # исправлено
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.kheshirovanny_parol):  # исправлено
        raise HTTPException(status_code=401, detail="Неверный email или пароль")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}