import os
import json
import bcrypt
import jwt
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import List

# Secret key to encode/decode JWT (should be kept secret)
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# In-memory user data and leaderboard
users_db = {}  # For storing registered users
leaderboard = []  # For storing the leaderboard
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# FastAPI instance
app = FastAPI()

# Pydantic models
class User(BaseModel):
    username: str
    password: str

class Score(BaseModel):
    username: str
    score: int

# Utility function to hash passwords
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Utility function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to get current user from the JWT token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    return username

# Register a new user
@app.post("/register")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(user.password)
    users_db[user.username] = {"password": hashed_password, "score": 0}
    
    return {"msg": "User registered successfully"}

# Login user and return JWT token
@app.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Submit a score
@app.post("/submit-score")
def submit_score(score: Score, current_user: str = Depends(get_current_user)):
    if score.username != current_user:
        raise HTTPException(status_code=400, detail="You cannot submit a score for another user")
    
    # Save the score and timestamp
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
    leaderboard.append({"username": score.username, "score": score.score, "timestamp": timestamp})
    
    # Keep leaderboard sorted by score
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    return {"msg": "Score submitted successfully", "timestamp": timestamp}

# Get leaderboard
@app.get("/leaderboard", response_model=List[Score])
def get_leaderboard():
    return leaderboard

# Logout - Remove the token from the client side (client needs to handle)
@app.post("/logout")
def logout():
    return {"msg": "Logged out successfully. Remove token from client storage."}
    