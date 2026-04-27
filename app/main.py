from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, categories, transactions
from app.db.init_db import init_db

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(transactions.router)


@app.on_event("startup")
def on_startup():
    init_db()