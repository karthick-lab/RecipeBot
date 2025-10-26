def calculate_total_cost(priced_df, num_pieces):
    raw_total = sum([
        row['TotalCost'] for _, row in priced_df.iterrows()
        if row['TotalCost'] != "Unknown"
    ])
    packing = num_pieces * 15
    overhead = 50 + 150 + 100 + 50
    total = raw_total + packing + overhead
    selling_price = round(total * 1.3, 2)

    return {
        "RawMaterialCost": raw_total,
        "PackingCost": packing,
        "Overhead": overhead,
        "TotalCost": total,
        "SellingPrice": selling_price
    }