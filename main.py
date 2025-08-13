from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os

app = FastAPI()

USERS_FILE = "users.json"

# Create the JSON file if not exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump([], f)

class RegisterUser(BaseModel):
    full_name: str
    username: str
    password: str

class LoginUser(BaseModel):
    username: str
    password: str

def read_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def write_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

@app.post("/register")
def register_user(user: RegisterUser):
    users = read_users()

    # Check if username already exists
    if any(u["username"] == user.username for u in users):
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = {
        "full_name": user.full_name,
        "username": user.username,
        "password": user.password
    }
    users.append(new_user)
    write_users(users)

    return {"message": "User registered successfully"}

@app.post("/login")
def login_user(user: LoginUser):
    users = read_users()

    for u in users:
        if u["username"] == user.username and u["password"] == user.password:
            return {"message": "Login successful"}
    
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/users")
def get_all_users():
    return read_users()
