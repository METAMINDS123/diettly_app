import React, { useState } from "react";

function App() {
  const [profile, setProfile] = useState({
    age: 25,
    weight: 65,
    height: 170,
    health_conditions: [],
    allergies: [],
  });
  const [preferences, setPreferences] = useState({
    diet_type: "Veg",
    cuisines: ["Indian"],
    fasting_mode: "",
  });
  const [pantry, setPantry] = useState({ ingredients: ["quinoa", "banana"] });
  const [mealPlan, setMealPlan] = useState();
  const [missing, setMissing] = useState([]);
  const [orderStatus, setOrderStatus] = useState();

  async function fetchMealPlan() {
  const payload = { profile, preferences, pantry };
  console.log("🚀 Sending payload to /mealplan:", payload);  // ← log here

  const res = await fetch("http://localhost:8000/mealplan", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await res.json();
  setMealPlan(data);
  setMissing(data.missing_ingredients);
}

  async function orderMissing() {
    const res = await fetch("http://localhost:8000/blinkit/order", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ missing_ingredients: missing }),
    });
    const data = await res.json();
    setOrderStatus(data.status);
  }

  return (
    <div style={{ padding: 30 }}>
      <h1>Diettly AI Agent Demo</h1>
      <button onClick={fetchMealPlan}>Generate Meal Plan</button>
      {mealPlan && (
        <div>
          <h2>Meals</h2>
          {mealPlan.meals &&
            mealPlan.meals.map((m) => (
              <div key={m.name}>
                <b>{m.name}</b> - {m.macros.calories} kcal
                <br />
                Ingredients: {m.ingredients.join(", ")}
                <br />
                Instructions: {m.instructions}
                <hr />
              </div>
            ))}
          <h3>Snacks</h3>
          {mealPlan.snacks &&
            mealPlan.snacks.map((s) => <div key={s.name}>{s.name}</div>)}
          <h3>
            Missing Ingredients: {missing && missing.length ? missing.join(", ") : "None"}
          </h3>
          <button onClick={orderMissing} disabled={!missing.length}>
            Order Missing (Blinkit Sim)
          </button>
          <div>{orderStatus}</div>
        </div>
      )}
    </div>
  );
}

export default App;
