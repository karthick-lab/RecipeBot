def parse_recipe(text):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    recipe = {
        "title": "Untitled Recipe",
        "method": "Unknown",
        "cook_time": "Unknown",
        "ingredients": [],
        "steps": [],
        "timestamp": "now"
    }

    try:
        for line in lines:
            if line.lower().startswith("title:"):
                recipe["title"] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("method:"):
                recipe["method"] = line.split(":", 1)[1].strip()
            elif line.lower().startswith("cook time:"):
                recipe["cook_time"] = line.split(":", 1)[1].strip()
            elif line.lower() == "ingredients:":
                ing_start = lines.index(line) + 1
            elif line.lower() == "steps:":
                step_start = lines.index(line) + 1
                break
        else:
            ing_start = step_start = len(lines)

        # Parse ingredients
        for line in lines[ing_start:step_start - 1]:
            if ":" in line:
                name, qty = line.split(":", 1)
                try:
                    qty_val = int(''.join(filter(str.isdigit, qty)))
                except:
                    qty_val = 0
                recipe["ingredients"].append({
                    "name": name.strip(),
                    "qty": qty_val,
                    "unit": "g"
                })

        # Parse steps
        for line in lines[step_start:]:
            recipe["steps"].append(line)

    except Exception as e:
        print("⚠️ Failed to parse recipe:", e)
        print("Raw response:\n", text)

    return recipe