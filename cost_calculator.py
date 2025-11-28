def calculate_total_cost(priced_df, num_pieces):
    print("📊 Columns in priced_df (inside cost calculator):", priced_df.columns.tolist())

    if "totalcost" not in priced_df.columns:
        raise ValueError("❌ 'totalcost' column missing in priced_df. Check ingredient_pricer.py.")

    ingredient_total = 0.0
    for _, row in priced_df.iterrows():
        value = row["totalcost"]
        if isinstance(value, (int, float)):
            ingredient_total += value

    # ✅ Fixed overheads
    labour = 100.0
    rent = 100.0
    gas = 50.0
    electricity = 50.0

    # ✅ Packing and profit remain unchanged
    packing = float(num_pieces) * 20.0
    profit = round(ingredient_total * 0.25, 2)

    final = round(ingredient_total + labour + rent + gas + electricity + packing + profit, 2)

    return {
        "Ingredient Cost": round(ingredient_total, 2),
        "Labour": labour,
        "Rent": rent,
        "Gas": gas,
        "Electricity": electricity,
        "Packing": packing,
        "Profit (25%)": profit,
        "Final Cost": final
    }