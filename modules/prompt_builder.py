def build_prompt(dish_type, key_ingredients, extra_ingredients, tray_size=None):
    all_ingredients = key_ingredients + extra_ingredients
    ingredient_list = ", ".join(all_ingredients)

    prompt = (
        f"You are a culinary expert. Generate a {dish_type} recipe using the following ingredients: {ingredient_list}.\n"
    )

    if tray_size:
        prompt += f"The recipe should be portioned for a tray of size {tray_size} inches.\n"

    prompt += (
        "Format the output exactly as follows:\n"
        "Title: <recipe name>\n"
        "Method: <cooking method>\n"
        "Cook Time: <duration>\n"
        "Ingredients:\n"
        "- <ingredient>: <quantity in grams>\n"
        "Steps:\n"
        "1. <step 1>\n"
        "2. <step 2>\n"
        "...\n"
        "Keep the recipe concise and suitable for real-world kitchen use."
    )

    return prompt