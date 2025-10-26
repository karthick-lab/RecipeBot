import pandas as pd
import random
from datetime import datetime

def generate_recipe(master_path, existing_titles):
    # Load known ingredients from Excel

    print("✅ Calling generate_recipe...")

    try:
        master_df = pd.read_excel(master_path)
        known_ingredients = master_df['Ingredient'].dropna().str.lower().tolist()
    except Exception as e:
        print(f"Error loading ingredient master: {e}")
        return None

    # Select 3 known ingredients
    selected_known = random.sample(known_ingredients, min(3, len(known_ingredients)))

    # Add 1 new ingredient
    new_ingredient = f"new_ingredient_{random.randint(100,999)}"
    all_ingredients = selected_known + [new_ingredient]

    # Generate unique title
    title = f"{selected_known[0].title()} Fusion Delight"
    if title in existing_titles:
        return None  # Skip duplicates

    # Build recipe object
    recipe = {
        "title": title,
        "method": "Baking" if "baking soda" in all_ingredients else "Stove",
        "baking_temp": "180°C" if "baking soda" in all_ingredients else None,
        "cook_time": "25 minutes" if "baking soda" in all_ingredients else "15 minutes",
        "ingredients": [{"name": ing, "qty": random.randint(50, 200), "unit": "g"} for ing in all_ingredients],
        "steps": [
            "Prep all ingredients.",
            "Mix and cook based on method.",
            "Serve hot."
        ],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    print("✅ Recipe generated:")

    return recipe