'''
from pydantic import BaseModel
from typing import List, Optional

class UserProfile(BaseModel):
    age: int
    weight: float
    height: float
    health_conditions: Optional[List[str]] = []
    allergies: Optional[List[str]] = []

class Preferences(BaseModel):
    diet_type: str
    cuisines: List[str]
    fasting_mode: Optional[str] = None

class Pantry(BaseModel):
    ingredients: List[str]

class MealPlanRequest(BaseModel):
    profile: UserProfile
    preferences: Preferences
    pantry: Pantry

class Meal(BaseModel):
    name: str
    ingredients: List[str]
    instructions: str
    macros: dict

class MealPlanResponse(BaseModel):
    meals: List[Meal]
    snacks: List[Meal]
    missing_ingredients: List[str]
'''



'''
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class UserProfile(BaseModel):
    age: int
    weight: float
    height: float
    health_conditions: Optional[List[str]] = Field(default_factory=list)
    allergies: Optional[List[str]] = Field(default_factory=list)

class Preferences(BaseModel):
    diet_type: str
    cuisines: List[str]
    fasting_mode: Optional[str] = None

class Pantry(BaseModel):
    ingredients: List[str]

class MealPlanRequest(BaseModel):
    profile: UserProfile
    preferences: Preferences
    pantry: Pantry

class Meal(BaseModel):
    name: str
    ingredients: List[str]
    instructions: str
    macros: Dict[str, float]

class MealPlanResponse(BaseModel):
    meals: List[Meal]
    snacks: List[Meal]
    missing_ingredients: List[str]

class BlinkitOrderRequest(BaseModel):
    missing_ingredients: List[str]







#how to use 
#from models import UserProfile, Preferences, Pantry, MealPlanRequest, Meal, MealPlanResponse, BlinkitOrderRequest


'''








# database.py
from sqlmodel import SQLModel, Field
from typing import Optional, List, Dict



class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str  # NOTE: hash this in production

class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    age: int
    weight: float
    height: float
    health_conditions: Optional[str] = None  # comma-separated
    allergies: Optional[str] = None
    diet_type: str
    cuisines: Optional[str] = None  # comma-separated
    fasting_mode: Optional[str] = None
    pantry: Optional[str] = None  # comma-separated
    user_id: int = Field(foreign_key="user.id")

class Preferences(SQLModel):
    diet_type: str
    cuisines: List[str]
    fasting_mode: Optional[str] = None

class Pantry(SQLModel):
    ingredients: List[str]

class MealPlanRequest(SQLModel):
    profile: UserProfile
    preferences: Preferences
    pantry: Pantry

class Meal(SQLModel):
    name: str
    ingredients: List[str]
    instructions: str
    macros: Dict[str, float]

class MealPlanResponse(SQLModel):
    meals: List[Meal]
    snacks: List[Meal]
    missing_ingredients: List[str]    

# main.py
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from backend.models import User, UserProfile
from backend.database import engine, init_db
from pydantic import BaseModel
from typing import List

init_db()

app = FastAPI()

class RegisterUser(BaseModel):
    name: str
    email: str
    password: str

@app.post("/register")
def register_user(user: RegisterUser):
    with Session(engine) as session:
        existing = session.exec(select(User).where(User.email == user.email)).first()
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")
        new_user = User(**user.dict())
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

class SaveProfile(BaseModel):
    user_id: int
    age: int
    weight: float
    height: float
    health_conditions: List[str]
    allergies: List[str]
    diet_type: str
    cuisines: List[str]
    fasting_mode: str
    pantry: List[str]

@app.post("/save-profile")
def save_profile(profile: SaveProfile):
    with Session(engine) as session:
        user = session.get(User, profile.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        profile_db = UserProfile(
            age=profile.age,
            weight=profile.weight,
            height=profile.height,
            health_conditions=",".join(profile.health_conditions),
            allergies=",".join(profile.allergies),
            diet_type=profile.diet_type,
            cuisines=",".join(profile.cuisines),
            fasting_mode=profile.fasting_mode,
            pantry=",".join(profile.pantry),
            user_id=user.id
        )
        session.add(profile_db)
        session.commit()
        session.refresh(profile_db)
        return profile_db

@app.get("/profile/{user_id}")
def get_profile(user_id: int):
    with Session(engine) as session:
        profile = session.exec(select(UserProfile).where(UserProfile.user_id == user_id)).first()
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile