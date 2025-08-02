# diettly_app
# 🧠 Diettly – AI-Powered Personalized Meal Planner 🍽️

Diettly is a conversational meal planning app that intelligently crafts daily meal plans based on your personal health metrics, dietary restrictions, cuisine preferences, fasting practices, and what's in your kitchen. It even checks your pantry, recommends missing ingredients, and can suggest ordering through Blinkit.

Built for modern nutrition enthusiasts, health-focused users, and anyone who wants to eat smart — all powered by AI.

---

## 🚀 Features

- 👤 Collects user details: age, weight, height, health conditions (Diabetes, PCOD, allergies, etc.)
- 🥗 Supports dietary preferences: Veg, Vegan, Keto, etc.
- 🌍 Cuisine selection: Indian, Mediterranean, Asian, and more
- ⏱️ Fasting types: Intermittent, OMAD, etc.
- 🥣 Personalized meal plan: 3 meals (Breakfast, Lunch, Dinner) + 2 Snacks
- 🧾 Auto-generates: Ingredients, Cooking instructions, Macros (calories, protein, carbs, fat)
- 📦 Pantry check: Tracks your available ingredients
- 🧠 Built with FastAPI + Streamlit + LangChain + SQLite

---

## 📁 Project Structure

PROJECT_DIETTLY/
│
├── backend/
│   ├── _pycache_/
│   │   ├── _init_.cpython-313.pyc
│   │   ├── database.cpython-313.pyc
│   │   ├── main.cpython-313.pyc
│   │   └── models.cpython-313.pyc
│   │
│   ├── services/
│   │   ├── _pycache_/
│   │   │   ├── _init_.cpython-313.pyc
│   │   │   ├── mealplan_generator.cpython-313.pyc
│   │   │   └── pantry_utils.cpython-313.pyc
│   │   ├── _init_.py
│   │   ├── consent.py
│   │   ├── mealplan_generator.py
│   │   └── pantry_utils.py
│   │
│   ├── _init_.py
│   ├── database.py
│   ├── main.py
│   ├── meal_llm.py
│   └── models.py
│
├── frontend/
│   └── diettly-frontend/
│       ├── public/
│       └── src/
│           ├── components/
│           ├── api.js
│           └── App.js
│       └── package.json
│
├── streamlit_prototype/
│   ├── utils/
│   ├── chat_agent.py
│   └── diettly_app.py
│
├── .env
├── .gitignore
├── diettly.db
├── requirement.txt
└── README.md





📌 How It Works
1. You input personal health info, dietary style, cuisines, and pantry items.

2. LangChain + OpenAI GPT generates:

   *  Breakfast, Lunch, Dinner

   *  Morning and Evening Snacks

   *  Calories, Macros, and Instructions

3. Missing ingredients are detected from pantry list.

4. Recipes and macros are displayed in Streamlit.

5. User profiles are saved locally using SQLite.


🧪 Example API Usage
/register – Register User

POST /register
{
  "name": "Aldi",
  "email": "aldi@example.com",
  "password": "secure123"
}


/mealplan – Generate Personalized Plan

POST /mealplan
{
  "age": 25,
  "weight": 70,
  "height": 172,
  "health_conditions": ["PCOD"],
  "diet_type": "Vegan",
  "cuisines": "Indian",
  "fasting_mode": "Intermittent",
  "pantry": ["rice", "tofu", "spinach"]
}

💾 Database
The project uses SQLite (diettly.db) to store:

Registered users

User profiles

Tables are auto-created on first launch via SQLModel

You can explore the DB using DB Browser for SQLite


🧠 Powered By
* FastAPI

* Streamlit

* LangChain

* OpenAI GPT-4

* SQLite + SQLModel

📄 License
MIT License – use it freely, contribute gladly.


   
