import os

DISH_FILE = "data/generated_dishes.txt"

def ensure_dish_file_exists(file_path="data/generated_dishes.txt"):
    folder = os.path.dirname(file_path)
    if not os.path.exists(folder):
        os.makedirs(folder)  # ✅ Create the 'data/' folder if missing
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")

def load_previous_dishes(file_path=DISH_FILE):
    ensure_dish_file_exists(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_new_dish(dish_name, file_path=DISH_FILE):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(dish_name.strip() + "\n")

