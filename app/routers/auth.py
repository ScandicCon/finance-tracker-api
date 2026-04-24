from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas.auth import TokenResponse, RegisterRequest
from app.schemas.users import UserResponse
from app.db.session import get_db
from app.models.users import User
from app.core.secutity import verify_password, create_token, hash_password

router = APIRouter(prefix="auth", tags=["AUTH"])


@router.post("login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    stmt = select(User).where(User.email == form_data.username)
    user = session.execute(stmt).scalar_one_or_none()

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_token({"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )

@router.post("/register", response_model=UserResponse)
def register(data_user: RegisterRequest, session: Session = Depends(get_db) ):
    stmt = select(User).where(User.email == data_user.email)
    user = session.execute(stmt).scalar_one_or_none()
    if user:
         raise HTTPException(status_code=409, detail="User with this email already exists")
    hashed_password = hash_password(data_user.password)
    users = User(
        email = data_user.email,
        username = data_user.username,
        hashed_password = hashed_password
    )
    session.add(users)
    session.commit()
    session.refresh(users)
    return users