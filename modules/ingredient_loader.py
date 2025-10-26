import pandas as pd

def get_key_ingredients(master_path):
    try:
        df = pd.read_excel(master_path)
        return df['Ingredient'].dropna().str.lower().tolist()
    except Exception as e:
        print(f"Error loading ingredients: {e}")
        return []