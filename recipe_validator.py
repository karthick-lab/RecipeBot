import re

def is_valid_ingredient_line(line):
    # Must contain ":" and a unit, and not be a section header
    if ":" not in line:
        return False
    if any(line.lower().startswith(prefix) for prefix in [
        "ingredients:", "setup:", "boil:", "rest:", "serve:", "step",
        "title:", "type:", "method:", "cook time:"
    ]):
        return False
    return any(unit in line.lower() for unit in ["g", "ml", "pieces", "teaspoon", "tablespoon"])

def ingredient_used_in_steps(ingredient_line, steps):
    # Extract the ingredient name before the colon
    name = ingredient_line.split(":")[0].lower().strip()
    return any(name in step.lower() for step in steps)

def validate_recipe(recipe):
    issues = []

    # Check metadata
    if not recipe.get("title"):
        issues.append("Missing title in metadata.")
    if not recipe.get("type"):
        issues.append("Missing dish type in metadata.")
    if not recipe.get("method"):
        issues.append("Missing method in metadata.")
    if not recipe.get("cook_time"):
        issues.append("Missing cook time in metadata.")

    # Check ingredient usage
    ingredients = recipe.get("ingredients", [])
    steps = recipe.get("steps", [])

    for ing in ingredients:
        if not is_valid_ingredient_line(ing):
            continue  # Skip section headers or malformed lines
        if not ingredient_used_in_steps(ing, steps):
            issues.append(f"Ingredient '{ing}' not used in any step.")

    return issues