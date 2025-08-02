// src/components/api.js

// Update this base URL if your backend is elsewhere
const BASE_URL = "http://localhost:8000";

/**
 * Helper for fetch with error handling and JSON parsing.
 */
async function fetchJSON(url, options = {}) {
  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return res.json();
}

/**
 * Get BMI from backend (POST /profile/bmi)
 * @param {Object} profile - { age, weight, height, allergies, health_conditions }
 * @returns {Object} - { bmi: ... }
 */
export async function getBMI(profile) {
  return fetchJSON(`${BASE_URL}/profile/bmi`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });
}

/**
 * Generate a meal plan (POST /mealplan)
 * @param {Object} profile
 * @param {Object} preferences
 * @param {Object} pantry
 * @returns {Object} - meal plan response from backend
 */
export async function generateMealPlan(profile, preferences, pantry) {
  return fetchJSON(`${BASE_URL}/mealplan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ profile, preferences, pantry }),
  });
}

/**
 * Order missing ingredients via Blinkit sim (POST /blinkit/order)
 * @param {Array} missingIngredients
 * @returns {Object} - simulated order status from backend
 */
export async function orderMissingIngredients(missingIngredients) {
  return fetchJSON(`${BASE_URL}/blinkit/order`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ missing_ingredients: missingIngredients }),
  });
}
