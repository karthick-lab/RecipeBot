from config_loader import load_config
from dish_tracker import load_previous_dishes


def build_recipe_prompt(dish_type, key_ingredients, extra_ingredients, tray_size=None, verified_context=None):
    # Always refresh previous dishes

    CONFIG = load_config()

    main_dish_prompt = CONFIG["main_dish_prompt"]
    masala_manufacturing_prompt = CONFIG["masala_manufacturing_prompt"]
    side_dish_prompt = CONFIG["side_dish_prompt"]
    beverage_powder_manufacturing_prompt= CONFIG["beverage_powder_manufacturing_prompt"]
    dessert_baking_prompt= CONFIG["dessert_baking_prompt"]
    snacks_prompt = CONFIG["snacks_prompt"]
    fruit_juices_prompt = CONFIG["fruit_juices_prompt"]
    breweries_prompt = CONFIG["breweries_prompt"]


    previous_dishes = load_previous_dishes()

    tray_text = f"Use a tray size of {tray_size} if relevant." if tray_size else ""
    context_text = f"\nContextual guidance: {verified_context}" if verified_context else ""

    piece_based = [
        "eggs", "egg", "banana", "bananas", "bread slice", "lemon",
        "paneer block", "chapati", "idli", "dosa"
    ]
    piece_instruction = ", ".join(piece_based)
    extra_prompt=""
    print("inside prompt builder"+dish_type)
    if(dish_type=="Main dish"):
        print("main dish identified")
        extra_prompt=main_dish_prompt

    elif(dish_type=="Masala manufacturing"):
        print("masala manufacturing identified")
        extra_prompt =masala_manufacturing_prompt

    elif (dish_type == "Side dish"):
        print("side dish identified")
        extra_prompt = side_dish_prompt

    elif (dish_type == "Beverage powder manufacturing"):
        print("Beverage powder identified")
        extra_prompt = beverage_powder_manufacturing_prompt

    elif (dish_type == "Dessert/Baking"):
        print("dessert/baking identified")
        extra_prompt = dessert_baking_prompt


    elif (dish_type == "Snacks"):
        print("snacks identified")
        extra_prompt = snacks_prompt


    elif (dish_type == "Fruit juices"):
        print("snacks identified")
        extra_prompt = fruit_juices_prompt


    elif (dish_type == "Breweries"):
        print("snacks identified")
        extra_prompt = breweries_prompt

    prompt = f"""
You are a professional recipe developer working for a restaurant R&D bot. Create a unique, realistic recipe for a {dish_type.lower()} {extra_prompt} using the following ingredients:

Exclude the following dishes that have already been generated:
{', '.join(previous_dishes)}

Seperate only Yield, Ingredients and Steps section by \n!!!!! at the end of mentioned sections
Use the same naming conventions as in Core ingredients and Optional extras below.

- Core ingredients: {', '.join(key_ingredients)}
- Optional extras: {', '.join(extra_ingredients) if extra_ingredients else 'None'}
- Not mandatory to use all the ingredients use only the necessary ingredients
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
- List each ingredient with realistic units (e.g. 2 : eggs, 100g : flour)

Steps:  
1. Step-by-step instructions using the listed ingredients


"""

    return prompt.strip()