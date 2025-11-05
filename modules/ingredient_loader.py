import pandas as pd

def get_key_ingredients(master_path):
    try:
        df = pd.read_excel(master_path)
        return df['Ingredient'].dropna().str.lower().tolist()
    except Exception as e:
        print(f"Error loading ingredients: {e}")
        return []

def strict_filter_by_dish_type(ingredients, dish_type, master_path):
    try:
        df = pd.read_excel(master_path)
        df["Ingredient"] = df["Ingredient"].str.lower()
        df["Dish Type Tags"] = df["Dish Type Tags"].fillna("").str.lower()

        # Filter ingredients that match the dish type or are tagged as "all"
        allowed = df[
            df["Dish Type Tags"].str.contains(dish_type.lower()) |
            df["Dish Type Tags"].str.contains("all")
        ]["Ingredient"].tolist()

        # Return only ingredients that are both in the master list and allowed for this dish type
        return [ing for ing in ingredients if ing.lower() in allowed]

    except Exception as e:
        print(f"Error filtering by dish type: {e}")
        return ingredients  # fallback: return all if filtering fails