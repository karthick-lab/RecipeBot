import tkinter as tk
from tkinter import ttk, messagebox
from modules.ingredient_loader import get_key_ingredients
from modules.prompt_builder import build_prompt
from connectors.mistral_connector import query_mistral
from connectors.gemini_connector import query_gemini
from modules.ingredient_pricer import price_ingredients
from modules.cost_calculator import calculate_total_cost
from modules.recipe_logger import log_recipe

master_path = r"C:\Users\admin\Desktop\Reports\Recipe maker\ingredient_master.xlsx"

class RnDBotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant R&D Bot")
        self.root.geometry("750x700")
        self.root.configure(bg="#fef9e7")

        self.recipe = None
        self.priced_df = None
        self.cost_summary = None
        self.tray_width = 0
        self.tray_height = 0
        self.num_pieces = 0
        self.piece_size = "N/A"

        self.build_ui()

    def build_ui(self):
        ttk.Label(self.root, text="🍽️ Restaurant R&D Bot", font=("Helvetica", 20, "bold")).pack(pady=10)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        # Dish type
        ttk.Label(form_frame, text="Type of Dish:").grid(row=0, column=0, padx=5, pady=5)
        self.dish_type = ttk.Combobox(form_frame, values=["Main Dish", "Side Course", "Baking", "Dessert"], state="readonly")
        self.dish_type.grid(row=0, column=1, padx=5)
        self.dish_type.set("Main Dish")

        # Model source
        ttk.Label(form_frame, text="Model Source:").grid(row=1, column=0, padx=5, pady=5)
        self.source_selector = ttk.Combobox(form_frame, values=["Mistral", "Gemini"], state="readonly")
        self.source_selector.grid(row=1, column=1, padx=5)
        self.source_selector.set("Mistral")

        # Optional ingredients
        ttk.Label(form_frame, text="Extra Ingredients (comma-separated):").grid(row=2, column=0, padx=5, pady=5)
        self.extra_ingredients_entry = ttk.Entry(form_frame, width=40)
        self.extra_ingredients_entry.grid(row=2, column=1, padx=5)

        # Tray dimensions
        ttk.Label(form_frame, text="Tray Width (in):").grid(row=3, column=0, padx=5, pady=5)
        self.width_entry = ttk.Entry(form_frame)
        self.width_entry.grid(row=3, column=1, padx=5)

        ttk.Label(form_frame, text="Tray Height (in):").grid(row=4, column=0, padx=5, pady=5)
        self.height_entry = ttk.Entry(form_frame)
        self.height_entry.grid(row=4, column=1, padx=5)

        # Buttons
        ttk.Button(self.root, text="Generate Recipe", command=self.generate).pack(pady=10)
        self.output = tk.Text(self.root, height=20, width=90, bg="#fcf3cf", font=("Courier", 10))
        self.output.pack(pady=10)
        ttk.Button(self.root, text="Save to Excel", command=self.save).pack(pady=5)

    def generate(self):
        dish = self.dish_type.get()
        source = self.source_selector.get()

        # Tray size required only for Baking or Dessert
        if dish in ["Baking", "Dessert"]:
            try:
                self.tray_width = float(self.width_entry.get())
                self.tray_height = float(self.height_entry.get())
                tray_size = f"{self.tray_width} x {self.tray_height}"
            except ValueError:
                messagebox.showerror("Input Error", "Tray size is required for Baking or Dessert.")
                return
        else:
            self.tray_width = 0
            self.tray_height = 0
            tray_size = None

        # Load ingredients
        key_ingredients = get_key_ingredients(master_path)
        extra_raw = self.extra_ingredients_entry.get()
        extra_ingredients = [i.strip().lower() for i in extra_raw.split(",") if i.strip()] if extra_raw else []

        # Build prompt
        prompt = build_prompt(dish, key_ingredients, extra_ingredients, tray_size)

        # Query model
        if source == "Mistral":
            self.recipe = query_mistral(prompt)
            target_path = r"C:\Users\admin\Desktop\Reports\Recipe maker\mistral_generated.xlsx"
        else:
            self.recipe = query_gemini(prompt)
            target_path = r"C:\Users\admin\Desktop\Reports\Recipe maker\gemini_generated.xlsx"

        if not self.recipe:
            self.output.insert(tk.END, "⚠️ No recipe generated.\n")
            return

        # Price and cost
        self.priced_df = price_ingredients(self.recipe["ingredients"], master_path)
        self.num_pieces = 10
        self.piece_size = "5x5"
        self.cost_summary = calculate_total_cost(self.priced_df, self.num_pieces)

        # Display
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"🍲 {self.recipe['title']}\n")
        self.output.insert(tk.END, f"Type: {dish}\n")
        self.output.insert(tk.END, f"Method: {self.recipe['method']}\n")
        self.output.insert(tk.END, f"Cook Time: {self.recipe['cook_time']}\n\n")

        self.output.insert(tk.END, "Ingredients:\n")
        for item in self.recipe["ingredients"]:
            self.output.insert(tk.END, f" - {item['name']} ({item['qty']} g)\n")

        self.output.insert(tk.END, "\nSteps:\n")
        for step in self.recipe["steps"]:
            self.output.insert(tk.END, f" - {step}\n")

        self.output.insert(tk.END, "\nCost Summary:\n")
        for key, value in self.cost_summary.items():
            self.output.insert(tk.END, f"{key}: ₹{value}\n")

        # Store path for saving
        self.target_path = target_path

    def save(self):
        if not self.recipe or not self.priced_df:
            messagebox.showerror("Save Error", "No recipe to save.")
            return

        log_recipe(
            self.recipe,
            self.priced_df,
            self.target_path,
            self.tray_width,
            self.tray_height,
            self.num_pieces,
            self.piece_size,
            self.cost_summary
        )
        messagebox.showinfo("Saved", f"Recipe saved to {self.target_path}")