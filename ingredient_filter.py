def strict_filter_by_dish_type(ingredients, dish_type):
    dish_map = {
        "Main Dish": {"rice", "wheat flour", "atta", "maida", "lentils", "onion", "tomato", "garam masala", "turmeric", "cumin", "chili powder", "ginger", "garlic"},
        "Dessert": {"flour", "sugar", "milk", "banana", "jaggery", "vanilla essence", "cocoa powder", "baking powder", "baking soda"},
        "Snack": {"potato", "bread", "egg", "besan", "poha", "corn", "chili flakes"}
    }
    allowed = dish_map.get(dish_type, set())
    return [ing for ing in ingredients if ing.lower() in allowed]