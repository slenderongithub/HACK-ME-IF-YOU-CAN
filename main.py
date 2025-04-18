from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError
import json
import uuid
from datetime import datetime, timedelta

app = FastAPI()

# JWT & security
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# User model
class User(BaseModel):
    username: str
    password: str

# Token model
class Token(BaseModel):
    access_token: str
    token_type: str

# Load or create user data
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

# Password hashing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# JWT creation
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Auth dependency
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Invalid token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        users = load_users()
        user = users.get(username)
        if not user:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

# Register
@app.post("/register")
def register(user: User):
    users = load_users()
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    users[user.username] = {
        "id": str(uuid.uuid4()),
        "username": user.username,
        "hashed_password": hash_password(user.password),
        "score": 0
    }
    save_users(users)
    return {"msg": "User registered successfully!"}

# Login
@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    users = load_users()
    user = users.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

# Submit score (protected)
@app.post("/submit-score")
def submit_score(score: int, current_user: dict = Depends(get_current_user)):
    users = load_users()
    username = current_user["username"]

    # Update if new score is higher
    if score > users[username]["score"]:
        users[username]["score"] = score
        save_users(users)
        return {"msg": "New high score saved!"}
    else:
        return {"msg": "Score not high enough to update."}

# Leaderboard
@app.get("/leaderboard")
def get_leaderboard():
    users = load_users()
    sorted_users = sorted(users.values(), key=lambda x: x["score"], reverse=True)

    leaderboard = []
    for idx, user in enumerate(sorted_users, start=1):
        leaderboard.append({
            "rank": idx,
            "username": user["username"],
            "score": user["score"]
        })

    return leaderboard
