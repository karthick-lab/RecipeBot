def classify_dish_type(ingredients):
    ingredient_set = set(ing.lower() for ing in ingredients)

    # Main Dish: rice, flour, lentils + spices
    if any(base in ingredient_set for base in ["rice", "wheat flour", "atta", "maida", "lentils"]) and \
       any(spice in ingredient_set for spice in ["garam masala", "turmeric", "cumin", "chili powder"]):
        return "Main Dish"

    # Dessert: flour + sweeteners/fruits
    if "flour" in ingredient_set and any(sweet in ingredient_set for sweet in ["banana", "jaggery", "sugar"]):
        return "Dessert"

    # Snack: bread, egg, potato, quick-fry items
    if any(snack in ingredient_set for snack in ["bread", "egg", "potato", "besan", "poha"]):
        return "Snack"

    return "Unknown"