import streamlit as st
import requests

st.title("Diet AI Planner (Streamlit UI)")

age = st.number_input("Age", min_value=13, max_value=90, step=1)
weight = st.number_input("Weight (kg)")
height = st.number_input("Height (cm)")
health_conditions = st.selectbox("Health Conditions", ["None","Diabities","Hypertension","PCOD/PCOS","High Cholestrol","Thyroid"])
allergies = st.selectbox("Allergies",["None","Nuts","Gluten","Lactose","Dairy","Egg","Grain","Peanut","Seafood","Sesame","Shellfish","Soy","Sulfite","Tree Nut","Wheat"])

diet_type = st.selectbox("Diet Type", ["Veg", "Non-Veg", "Vegan", "Keto", "No preference"])
cuisines = st.multiselect("Preferred cuisines", ["Indian", "Mediterranean", "Italian", "Chinese", "Global"])
fasting_mode = st.selectbox("Fasting mode", ["None", "Intermittent", "OMAD", "Custom"])

pantry_input = st.text_area("Ingredients you have (comma separated)")

if st.button("Generate Meal Plan"):
    payload = {
        "profile": {
            "age": age,
            "weight": weight,
            "height": height,
            "health_conditions": [x.strip() for x in health_conditions.split(",") if x.strip()],
            "allergies": [x.strip() for x in allergies.split(",") if x.strip()],
        },
        "preferences": {
            "diet_type": diet_type,
            "cuisines": cuisines,
            "fasting_mode": fasting_mode if fasting_mode != "None" else None,
        },
        "pantry": {
            "ingredients": [x.strip() for x in pantry_input.split(",") if x.strip()]
        }
    }
    try:
        response = requests.post("http://localhost:8000/mealplan", json=payload)
        if response.status_code == 200:
            meal_plan = response.json()
            st.write("### Meals:")
            for meal in meal_plan.get("meals", []):
                st.write(f"{meal['name']}** - {meal['macros']['calories']} kcal")
                st.write(f"Ingredients: {', '.join(meal['ingredients'])}")
                st.write(f"Instructions: {meal['instructions']}")
                st.write("---")


            st.write("### Snacks:")
            for snack in meal_plan.get("snacks", []):
                st.write(f"**{snack['name']}**")
            st.write("### Missing Ingredients:")
            st.write(", ".join(meal_plan.get("missing_ingredients", [])) or "None")
        else:
            st.error(f"API error: {response.status_code} {response.text}")
    except Exception as e:
        st.error(f"Could not connect to backend API: {e}")



#how to run

#pip install streamlit requests
#sstreamlit run app.py