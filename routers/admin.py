from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from model import Admin
from schema import AdminCreate,AdminList,ProblemWithUserSchema
from security import get_password_hash, authenticate_admin, create_access_token, get_current_admin,get_db
from fastapi.security import OAuth2PasswordRequestForm
from model import Problem, User
from security import get_current_admin
from typing import List

router = APIRouter()

router = APIRouter(
    tags = ["Admin"]
)



@router.post("/admins", status_code=status.HTTP_201_CREATED)
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    new_admin = Admin(email=admin.email, password=get_password_hash(admin.password), secret_key=admin.secret_key, district=admin.district)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return {"message": "Admin created successfully"}


@router.post("/login")
def login_admin(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    admin = authenticate_admin(db, form_data.username, form_data.password)
    db.close()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": admin.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/admins/me")
def get_current_admin(admin: Admin = Depends(get_current_admin)):
    return admin


@router.get("/admins", response_model=AdminList)
def get_all_admins(db: Session = Depends(get_db)):
    admin = db.query(Admin).all()
    return {"admins": admin}



@router.get("/admin/problems", response_model=List[ProblemWithUserSchema])
def get_all_user_problems_by_district_as_admin(district: str, db: Session = Depends(get_db)):
    # Get all problems for all users in the specified district
    problems = db.query(Problem).join(User).filter(User.district == district).all()
    return problems