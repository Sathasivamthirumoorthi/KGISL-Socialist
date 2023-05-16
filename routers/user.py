from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal
from model import User
from schema import UserCreate,UserList
from security import get_password_hash, authenticate_user, create_access_token, get_current_user,get_db

router = APIRouter(
    tags = ["User"]
)



@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(email=user.email, name=user.name, password=get_password_hash(user.password), phone=user.phone, district=user.district)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}


@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = authenticate_user(db, form_data.username, form_data.password)
    db.close()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
def get_current_user(user: User = Depends(get_current_user)):
    return user

@router.get("/users", response_model=UserList)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}