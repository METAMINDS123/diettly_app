# pantry_utils.py

from typing import List

def normalize_ingredient(item: str) -> str:
    # Lowercase, remove spaces, and any trivial normalization
    return item.lower().strip()

def clean_pantry_list(items: List[str]) -> List[str]:
    # Removes blanks, normalizes, and deduplicates entries
    return list(set(normalize_ingredient(it) for it in items if it.strip()))

def check_ingredients_in_pantry(required: List[str], pantry: List[str]) -> List[str]:
    pantry_clean = set(clean_pantry_list(pantry))
    missing = [r for r in required if normalize_ingredient(r) not in pantry_clean]
    return missing

def add_ingredient_to_pantry(ingredient: str, pantry: List[str]) -> List[str]:
    pantry_clean = clean_pantry_list(pantry)
    norm = normalize_ingredient(ingredient)
    if norm not in pantry_clean:
        pantry_clean.append(norm)
    return pantry_clean

def remove_ingredient_from_pantry(ingredient: str, pantry: List[str]) -> List[str]:
    norm = normalize_ingredient(ingredient)
    return [item for item in pantry if normalize_ingredient(item) != norm]