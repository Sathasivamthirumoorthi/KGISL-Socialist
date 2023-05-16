from pydantic import BaseModel
from typing import List
from typing import Optional

class AdminBase(BaseModel):
    email: str
    password: str


class AdminCreate(AdminBase):
    secret_key: str
    district: str


class Admin(AdminBase):
    id: int
    secret_key: str
    district: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    name: str
    password: str
    phone: str


class UserCreate(UserBase):
    district: str


class User(UserBase):
    id: int
    district: str

    class Config:
        orm_mode = True



class UserList(BaseModel):
    users: List[User]


class AdminList(BaseModel):
    admins : List[Admin]



class ProblemBase(BaseModel):
    image: str
    problem_statement: str
    phone: str
    district: str
    landmark: str
    name: str

class ProblemSchema(BaseModel):
    id: int
    image: str
    problem_statement: str
    phone: str
    district: str
    landmark: str
    name: str

    class Config:
        orm_mode = True

class ProblemCreate(ProblemBase):
    pass

class ProblemUpdate(ProblemBase):
    image: Optional[str] = None
    problem_statement: Optional[str] = None
    phone: Optional[str] = None
    district: Optional[str] = None
    landmark: Optional[str] = None
    name: Optional[str] = None
    

class UserSchema(BaseModel):
    id: int
    email: str
    name: str
    phone: str
    district: str

    class Config:
        orm_mode = True

class ProblemWithUserSchema(BaseModel):
    id: int
    image: str
    problem_statement: str
    phone: str
    district: str
    landmark: str
    name: str
    user: UserSchema

    class Config:
        orm_mode = True
