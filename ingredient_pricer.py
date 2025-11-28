import pandas as pd
import re

def normalize_unit(unit):
    unit = unit.lower()
    if "gram" in unit or unit == "g":
        return "g"
    elif "ml" in unit:
        return "ml"
    elif "piece" in unit or "pieces" in unit:
        return "piece"
    elif "teaspoon" in unit or "tsp" in unit:
        return "tsp"
    elif "tablespoon" in unit or "tbsp" in unit:
        return "tbsp"
    else:
        return unit

def simplify_name(name):
    name = name.lower().strip()

    # Keyword-based overrides
    keyword_map = {
        "rice": ["basmati", "long-grain", "short-grain", "steamed", "white rice", "brown rice"],
        "oil": ["sunflower", "vegetable", "refined", "mustard", "canola", "olive"],
        "salt": ["sea salt", "rock salt", "table salt"],
        "sugar": ["brown sugar", "white sugar", "powdered sugar", "jaggery"],
        "flour": ["maida", "atta", "whole wheat", "refined flour", "all-purpose"],
        "chili": ["green chili", "red chili", "chilli", "chili powder"],
        "onion": ["red onion", "white onion", "shallots"],
        "tomato": ["roma tomato", "cherry tomato", "fresh tomato"],
        "potato": ["baby potato", "sweet potato"],
        "milk": ["whole milk", "skimmed milk", "toned milk"],
        "curd": ["yogurt", "dahi"],
        "bread": ["white bread", "brown bread", "bun", "roll"],
        "egg": ["boiled egg", "whole egg", "egg white", "egg yolk"],
        "dal": ["toor dal", "moong dal", "masoor dal", "chana dal"],
        "garam masala": ["masala", "spice mix", "curry powder"],
        "vegetables": ["mixed vegetables", "seasonal vegetables", "fresh vegetables"],
    }

    for canonical, variants in keyword_map.items():
        if canonical in name:
            return canonical
        for variant in variants:
            if variant in name:
                return canonical

    return name

def price_ingredients(parsed_ingredients, master_path):
    # Load and normalize column names
    df = pd.read_excel(master_path)
    df.columns = [col.lower().strip() for col in df.columns]

    # Ensure required columns exist
    if "ingredient" not in df.columns:
        raise ValueError("❌ 'ingredient' column not found in master file.")
    if "price per kg" not in df.columns and "price per piece" not in df.columns:
        raise ValueError("❌ Pricing columns missing in master file.")

    df["ingredient"] = df["ingredient"].str.lower().str.strip()

    priced_rows = []

    for item in parsed_ingredients:
        name = simplify_name(item["name"])
        qty = item["qty"]
        unit = normalize_unit(item["unit"])

        match = df[df["ingredient"] == name]

        if not match.empty:
            row = match.iloc[0]
            if unit in ["g", "ml"]:
                price_per_kg = row.get("price per kg", 0.0)
                price_per_unit = price_per_kg / 1000
                cost = qty * price_per_unit
            elif unit == "piece":
                price_per_unit = row.get("price per piece", 0.0)
                cost = qty * price_per_unit
            else:
                price_per_unit = 0.0
                cost = 0.0
        else:
            print(f"❌ No match found for ingredient: '{name}'")
            price_per_unit = 0.0
            cost = 0.0

        priced_rows.append({
            "ingredient": name,
            "qty": qty,
            "unit": unit,
            "price_per_unit": price_per_unit,
            "totalcost": cost
        })

        print(f"✅ Priced: {name} | Qty: {qty} {unit} | ₹{cost:.2f}")

    priced_df = pd.DataFrame(priced_rows)
    print("📊 Columns in priced_df:", priced_df.columns.tolist())
    if "totalcost" not in priced_df.columns:
        print("❌ 'totalcost' column missing — check ingredient matching and fallback logic.")
    return priced_df