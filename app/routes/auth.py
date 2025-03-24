from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_access_token, verify_password, hash_password
from app.schemas import Token
from datetime import timedelta

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

fake_users_db = {}

@router.post("/register/")
async def register(username: str, password: str):
    if username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(password)
    fake_users_db[username] = hashed_password
    return {"message": "User created successfully"}

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if username not in fake_users_db:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    hashed_password = fake_users_db[username]
    if not verify_password(password, hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token = create_access_token(
        data={"sub": username}, expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}