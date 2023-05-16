from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.declarative import declarative_base
from routers import user, admin,problem
from model import Base
from database import engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# if table is not there , it will create one for us
Base.metadata.create_all(bind=engine)

# Include the user and admin routers
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(problem.router)
