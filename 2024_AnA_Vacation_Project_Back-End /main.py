from fastapi import FastAPI
from routers import users, codes
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(codes.router, prefix="/codes", tags=["codes"])


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
