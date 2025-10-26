import pandas as pd
import os
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

def log_recipe(recipe, priced_df, recipe_path, tray_width_in, tray_height_in, num_pieces, piece_size, cost_summary):
    sheet_name = recipe['title'][:31]

    # Create initial DataFrame with formulas
    df = pd.DataFrame(columns=["Ingredient", "Qty (g)", "PricePerKg", "TotalCost"])
    for i, item in enumerate(recipe["ingredients"]):
        ingredient = item["name"]
        qty = item["qty"]
        # Excel formula to lookup price from master sheet
        price_formula = f'=IFERROR(VLOOKUP("{ingredient}", [ingredient_master.xlsx]Sheet1!A:B, 2, FALSE), "Unknown")'
        total_formula = f'=IF(ISNUMBER(C{i+2}), B{i+2}/1000 * C{i+2}, "Unknown")'
        df.loc[i] = [ingredient, qty, price_formula, total_formula]

    # Summary
    summary_df = pd.DataFrame([{
        "Tray Size (in)": f"{tray_width_in} x {tray_height_in}",
        "Piece Size (cm)": piece_size,
        "Number of Pieces": num_pieces,
        "Raw Material Cost": f'=SUM(D2:D{len(df)+1})',
        "Packing Cost": cost_summary["PackingCost"],
        "Overhead": cost_summary["Overhead"],
        "Total Cost": f'=E{len(df)+3}+E{len(df)+4}+E{len(df)+5}',
        "Selling Price": f'=E{len(df)+6}*1.3'
    }])

    # Write to Excel
    file_exists = os.path.exists(recipe_path)
    with pd.ExcelWriter(recipe_path, engine='openpyxl', mode='a' if file_exists else 'w') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        summary_df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=len(df) + 3)