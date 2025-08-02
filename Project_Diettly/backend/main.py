'''
import os
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from backend.models import User, UserProfile
from backend.database import engine, init_db
from pydantic import BaseModel
from typing import List

# Import meal plan generation function from services (adjust if needed)
from backend.services.mealplan_generator import generate_meal_plan
app = FastAPI()
# -- Your Pydantic models (mirror your models.py) --
# You can import these if you already have them in models.py
class UserProfile(BaseModel):
    age: int
    weight: float
    height: float
    health_conditions: Optional[List[str]] = []
    allergies: Optional[List[str]] = []

class Preferences(BaseModel):
    diet_type: str  # e.g. "Veg", "Vegan", "Non-Veg"
    cuisines: Optional[List[str]] = []
    fasting_mode: Optional[str] = None

class Pantry(BaseModel):
    ingredients: List[str]

class Meal(BaseModel):
    name: str
    ingredients: List[str]
    instructions: str
    macros: Dict[str, float]  # calories, protein, carbs, fat

class MealPlanRequest(BaseModel):
    profile: UserProfile
    preferences: Preferences
    pantry: Pantry

class MealPlanResponse(BaseModel):
    meals: List[Meal]
    snacks: List[Meal]
    missing_ingredients: List[str]

# -- Initialize FastAPI app --
app = FastAPI(
    title="Diettly AI Agent API",
    description="Backend for Diettly — Personalized Meal Planning Agent",
    version="1.0.0"
)

# -- CORS middleware for frontend access --
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Diettly backend is running!"}

# Endpoint to generate meal plan
@app.post("/mealplan", response_model=MealPlanResponse)
async def get_meal_plan(request: MealPlanRequest):
    plan = generate_meal_plan(request)
    return plan


# Simulated Blinkit order endpoint (optional)
@app.post("/blinkit/order")
async def blinkit_order(missing_ingredients: List[str]):
    # For demo, just return a fake order confirmation
    return {
        "order_id": "BLINK123456",
        "items": missing_ingredients,
        "status": "Simulated order placed successfully."
    }

if __name__ == "__main__":
    import uvicorn
    # Read your API key here if you want to print or check env
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"Using OpenAI API Key: {'Set' if api_key else 'Not set'}")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

uvicorn backend.main:app --reload --port 8000
cd streamlit_prototype
streamlit run diettly_app.py 
'''


# backend/main.py
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
    
from backend.services.mealplan_generator import generate_meal_plan  # adjust import as needed
from backend.models import MealPlanRequest, MealPlanResponse

@app.post("/mealplan", response_model=MealPlanResponse)
async def get_meal_plan(request: MealPlanRequest):
    return generate_meal_plan(request)
   
