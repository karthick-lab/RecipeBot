def build_verified_context(snippet_text):
    lines = snippet_text.split(". ")
    ingredients = [line for line in lines if any(unit in line for unit in ["g", "cup", "tsp", "tablespoon"])]
    steps = [line for line in lines if line.lower().startswith(("add", "cook", "heat", "mix", "serve", "marinate", "layer", "boil", "sauté"))]

    return {
        "title": "Verified Recipe Reference",
        "ingredients": ingredients,
        "steps": steps,
        "cook_time": "60 minutes",
        "method": "Stove-top"
    }