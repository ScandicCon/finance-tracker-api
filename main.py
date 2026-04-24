from fastapi import FastAPI

from app.db.init_db import init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()