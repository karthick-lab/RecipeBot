import pandas as pd

def price_ingredients(recipe_ingredients, master_path):
    """
    Calculates price per ingredient based on quantity used in grams.
    Flags unknown prices for new ingredients.
    Returns a DataFrame with Ingredient, Qty, PricePerKg, and TotalCost.
    """
    try:
        master_df = pd.read_excel(master_path)
        price_map = dict(zip(master_df['Ingredient'].str.lower(), master_df['Price per pice or kg']))
    except Exception as e:
        print(f"Error reading ingredient master: {e}")
        price_map = {}

    priced = []
    for item in recipe_ingredients:
        name = item['name'].lower()
        qty = item['qty']  # in grams
        price = price_map.get(name, "Unknown")

        if price == "Unknown":
            total = "Unknown"
        else:
            try:
                total = round((qty / 1000) * float(price), 2)
            except Exception:
                total = "Unknown"

        priced.append({
            "Ingredient": item['name'],
            "Qty": f"{qty} g",
            "PricePerKg": price,
            "TotalCost": total
        })

    return pd.DataFrame(priced)