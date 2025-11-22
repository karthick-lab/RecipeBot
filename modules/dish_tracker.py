import json
import os
import sys

exe_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
config_file = os.path.join(exe_dir, "config.json")

with open(config_file, "r") as f:
    CONFIG = json.load(f)


DISH_FILE = CONFIG["generated_dishes_path"]

def ensure_dish_file_exists(file_path=CONFIG["generated_dishes_path"]):
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

