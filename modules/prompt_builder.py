


from modules.dish_tracker import load_previous_dishes, save_new_dish

# Load previously generated dishes
previous_dishes = load_previous_dishes()



def build_recipe_prompt(dish_type, key_ingredients, extra_ingredients, tray_size=None, verified_context=None):
    tray_text = f"Use a tray size of {tray_size} if relevant." if tray_size else ""
    context_text = f"\nContextual guidance: {verified_context}" if verified_context else ""

    piece_based = [
        "eggs", "egg", "banana", "bananas", "bread slice", "lemon", "green chili",
        "garlic clove", "paneer block", "chapati", "idli", "dosa"
    ]
    piece_instruction = ", ".join(piece_based)

    prompt = f"""
You are a professional recipe developer working for a restaurant R&D bot. Create a unique, realistic recipe for a {dish_type.lower()} dish using the following ingredients:

Exclude the following dishes that have already been generated:
{', '.join(previous_dishes)}

- Core ingredients: {', '.join(key_ingredients)}
- Optional extras: {', '.join(extra_ingredients) if extra_ingredients else 'None'}

Please include realistic portioning details such as:
- Number of pieces or servings
- Serving size in grams
- Cut dimensions (e.g., 5x5 inches squares or 50g portions)

Use realistic quantities:
- Use **grams (g)** for dry and liquid ingredients
- Use **pieces** for ingredients like: {piece_instruction}
- Do **not** list eggs or bananas in grams — convert to pieces (e.g., 2 eggs, 3 bananas)
- Avoid unrealistic weights like 1g egg or 2000g banana
{tray_text}
{context_text}

Respond using the following structure (do not include these labels as ingredients):

Title:  
Type:  
Method:  
Cook Time:  
Yield:  
- Include number of pieces, serving size in grams, or cut dimensions (e.g., 5x5 inches squares)

Ingredients:  
- List each ingredient with realistic units (e.g. 2 eggs, 100g flour)

Steps:  
1. Step-by-step instructions using the listed ingredients

Seperate each section by !!!!!
"""
    return prompt.strip()