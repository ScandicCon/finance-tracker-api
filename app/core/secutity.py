from datetime import datetime , timedelta, timezone
from pwdlib import PasswordHash
import jwt
from jwt import PyJWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from app.models.users import User


password_hashed = PasswordHash.recommended()

DUMMY_PASSWORD = "PASSWORDDUMMY"

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password:str):
    return password_hashed.hash(password)

def verify_password(plain_password: str, hash_password: str):
    return password_hashed.verify(plain_password, hash_password)

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(session: Session = Depends(get_db), token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_id = int(user_id)
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    stmt  = select(User).where(User.id == user_id)
    user = session.execute(stmt).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401)
    return user
