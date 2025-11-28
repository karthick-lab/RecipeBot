import pandas as pd
import random

def discover_dish_name(master_path, dish_type):
    df = pd.read_excel(master_path)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    if "dish type" not in df.columns or "ingredient" not in df.columns:
        return "Mixed Veg Curry"

    subset = df[df["dish type"] == dish_type.lower()]
    core_ingredients = subset["ingredient"].dropna().str.lower().tolist()

    archetypes = {
        "main dish": ["biryani", "curry", "masala", "pulao"],
        "side dish": ["dal", "sabzi", "poriyal", "chana"],
        "dessert/baking": ["cake", "pudding", "halwa", "bread"],
        "snacks": ["pakora", "cutlet", "roll", "poha"]
    }

    suffix = random.choice(archetypes.get(dish_type.lower(), ["fusion"]))
    prefix = random.choice(core_ingredients) if core_ingredients else "mixed"
    return f"{prefix.title()} {suffix.title()}"