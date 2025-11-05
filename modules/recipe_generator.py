import pandas as pd
import random
from datetime import datetime
from prompt_builder import build_prompt
from ingredient_filter import strict_filter_by_dish_type

def generate_recipe(master_path, existing_titles, mistral_generate_fn, user_dish_type, tray_size=None):
    print("✅ Calling generate_recipe...")

    # Load Excel ingredients
    try:
        master_df = pd.read_excel(master_path)
        all_excel_ingredients = master_df['Ingredient'].dropna().str.lower().tolist()
    except Exception as e:
        print(f"❌ Error loading ingredient master: {e}")
        return None

    # Strictly filter by dish type
    filtered_ingredients = strict_filter_by_dish_type(all_excel_ingredients, user_dish_type)

    # If not enough relevant ingredients, use fallback archetypes
    fallback_map = {
        "Main Dish": ["rice", "garam masala", "onion", "tomato"],
        "Dessert": ["flour", "sugar", "milk", "banana"],
        "Snack": ["potato", "bread", "besan", "egg"]
    }

    if len(filtered_ingredients) < 3:
        selected_ingredients = fallback_map.get(user_dish_type, [])
    else:
        selected_ingredients = random.sample(filtered_ingredients, min(3, len(filtered_ingredients)))

    # Add one new ingredient
    new_ingredient = f"new_ingredient_{random.randint(100,999)}"
    final_ingredients = selected_ingredients + [new_ingredient]

    # Build prompt using only final_ingredients
    prompt = build_prompt(user_dish_type, selected_ingredients, [new_ingredient], tray_size)
    mistral_response = mistral_generate_fn(prompt)

    if not mistral_response:
        print("❌ Mistral failed to generate recipe.")
        return None

    # Generate title
    title = mistral_response.get("Title", f"{selected_ingredients[0].title()} Fusion Delight" if selected_ingredients else "Fusion Delight")
    if title in existing_titles:
        print("⚠️ Duplicate title detected. Skipping.")
        return None

    # Parse ingredients
    parsed_ingredients = []
    for line in mistral_response.get("Ingredients", []):
        try:
            name, qty_str = line.split(":")
            qty = int(qty_str.strip().split()[0])
            parsed_ingredients.append({"name": name.strip(), "qty": qty, "unit": "g"})
        except:
            continue

    # Final recipe object
    recipe = {
        "title": title,
        "method": mistral_response.get("Method", "Unknown"),
        "cook_time": mistral_response.get("Cook Time", "Unknown"),
        "baking_temp": mistral_response.get("Baking Temperature", None),
        "ingredients": parsed_ingredients,
        "steps": mistral_response.get("Steps", []),
        "dish_type": user_dish_type,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    print("✅ Recipe generated successfully.")
    return recipe