from fastapi import FastAPI

from app.db.init_db import init_db
from app.routers import categories, auth, transactions



app = FastAPI()
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)



@app.on_event("startup")
def on_startup():
    init_db()