
import re
import os
import json
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from ..models import UserProfile, Preferences, Pantry, Meal, MealPlanResponse, MealPlanRequest

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # <-- Correct instantiation

def generate_meal_plan(request: MealPlanRequest) -> MealPlanResponse:
    profile = request.profile
    preferences = request.preferences
    pantry = request.pantry

    # Compose LLM prompt
    prompt = f"""
Generate a **healthy and safe** meal plan for the following user, strictly respecting their dietary restrictions and allergies.

User profile:
- Age: {profile.age}
- Height: {profile.height} cm
- Weight: {profile.weight} kg
- Reported health conditions: {', '.join(profile.health_conditions) if profile.health_conditions else 'None'}
- Allergies or intolerances: {', '.join(profile.allergies) if profile.allergies else 'None'}
- Diet type: {preferences.diet_type}
- Preferred cuisines: {', '.join(preferences.cuisines)}
- Pantry items: {', '.join(pantry.ingredients)}

Instructions:
- Do NOT include any ingredients or foods that conflict with the user's allergies or health conditions.
- Avoid cross-contamination risks in ingredient suggestions.
- Provide suitable substitutes for common allergens or restricted ingredients.
- If a health condition like diabetes, hypertension, or PCOS is present, tailor meals according to standard nutritional guidelines (e.g., low sugar for diabetes, low sodium for hypertension).
- Generate exactly 3 meals (breakfast, lunch, dinner) and 2 snacks.
- Provide the meal plan as **valid JSON only** with this exact structure:

{{
  "meals": [
    {{
      "name": "Meal Name",
      "ingredients": [...],
      "instructions": "...",
      "macros": {{
        "calories": number,
        "protein": number,
        "carbs": number,
        "fat": number
      }},
      "notes": "Any important notes on allergens or substitutions."
    }}
  ],
  "snacks": [
    {{
      "name": "Snack Name",
      "ingredients": [...],
      "instructions": "...",
      "macros": {{
        "calories": number,
        "protein": number,
        "carbs": number,
        "fat": number
      }},
      "notes": "Any important notes on allergens or substitutions."
    }}
  ],
  "missing_ingredients": [...]
}}

**No text outside of JSON. Use 'notes' to explain substitutions or allergen considerations only if needed.
Do NOT include units like 'g'.**
"""

    try:
        # GPT call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a nutritionist and meal planner."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1200
        )

        result_text = response.choices[0].message.content.strip()

        # Extract JSON only
        start = result_text.find('{')
        end = result_text.rfind('}') + 1
        cleaned_json = result_text[start:end]

        plan = json.loads(cleaned_json)

        # Validate and construct response
        meals = [
            Meal(
                name=m["name"],
                ingredients=m["ingredients"],
                instructions=m["instructions"],
                macros=m["macros"],
            ) for m in plan["meals"]
        ]
        snacks = [
            Meal(
                name=s["name"],
                ingredients=s["ingredients"],
                instructions=s["instructions"],
                macros=s["macros"]
            ) for s in plan["snacks"]
        ]
        missing_ingredients = plan.get("missing_ingredients", [])  # fallback if missing

        return MealPlanResponse(
            meals=meals,
            snacks=snacks,
            missing_ingredients=missing_ingredients
        )

    except Exception as e:
        # Log error and return fallback empty plan
        print("MealPlan generation failed:", str(e))
        return MealPlanResponse(
            meals=[],
            snacks=[],
            missing_ingredients=[f"AI Error: {str(e)}"]
        )
