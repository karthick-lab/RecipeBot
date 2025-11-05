import tkinter as tk
from tkinter import ttk, messagebox
import re

from modules.ingredient_loader import get_key_ingredients, strict_filter_by_dish_type
from modules.dish_discovery import discover_dish_name
from modules.prompt_builder import build_recipe_prompt
from modules.verified_context_builder import build_verified_context
from connectors.mistral_connector import query_mistral
from connectors.gemini_connector import query_gemini
from modules.ingredient_pricer import price_ingredients, simplify_name
from modules.cost_calculator import calculate_total_cost
from modules.recipe_logger import log_recipe
from modules.recipe_parser import parse_gemini_response

master_path = r"C:\Users\admin\Desktop\Reports\Recipe maker\ingredient_master.xlsx"
DISH_FILE = "data/generated_dishes.txt"


class RnDBotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant R&D Bot")
        self.root.geometry("750x700")
        self.root.configure(bg="#fef9e7")

        self.recipe = None
        self.recipe_title = None
        self.priced_df = None
        self.cost_summary = None
        self.tray_width = 0
        self.tray_height = 0
        self.num_pieces = 0
        self.serving_size = "N/A"

        self.build_ui()

    def build_ui(self):
        ttk.Label(self.root, text="🍽️ Restaurant R&D Bot", font=("Helvetica", 20, "bold")).pack(pady=10)

        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Type of Dish:").grid(row=0, column=0, padx=5, pady=5)
        self.dish_type = ttk.Combobox(form_frame, values=["Main dish", "Side dish", "Dessert/Baking", "Snacks"],
                                      state="readonly")
        self.dish_type.grid(row=0, column=1, padx=5)
        self.dish_type.set("Main dish")

        ttk.Label(form_frame, text="Model Source:").grid(row=1, column=0, padx=5, pady=5)
        self.source_selector = ttk.Combobox(form_frame, values=["Mistral", "Gemini"], state="readonly")
        self.source_selector.grid(row=1, column=1, padx=5)
        self.source_selector.set("Gemini")

        ttk.Label(form_frame, text="Extra Ingredients (comma-separated):").grid(row=2, column=0, padx=5, pady=5)
        self.extra_ingredients_entry = ttk.Entry(form_frame, width=40)
        self.extra_ingredients_entry.grid(row=2, column=1, padx=5)

        ttk.Label(form_frame, text="Tray Width (in):").grid(row=3, column=0, padx=5, pady=5)
        self.width_entry = ttk.Entry(form_frame)
        self.width_entry.grid(row=3, column=1, padx=5)

        ttk.Label(form_frame, text="Tray Height (in):").grid(row=4, column=0, padx=5, pady=5)
        self.height_entry = ttk.Entry(form_frame)
        self.height_entry.grid(row=4, column=1, padx=5)

        # ✅ Operational Expense % Dropdown
        ttk.Label(form_frame, text="Operational Expense %:").grid(row=5, column=0, padx=5, pady=5)
        self.operational_var = tk.StringVar()
        self.operational_dropdown = ttk.Combobox(
            form_frame,
            textvariable=self.operational_var,
            values=["100%", "75%", "50%", "30%", "25%", "15%", "10%"],
            state="readonly"
        )
        self.operational_dropdown.grid(row=5, column=1, padx=5)
        self.operational_dropdown.set("100%")

        ttk.Button(self.root, text="Generate Recipe", command=self.generate).pack(pady=10)
        self.output = tk.Text(self.root, height=20, width=90, bg="#fcf3cf", font=("Courier", 10))
        self.output.pack(pady=10)
        ttk.Button(self.root, text="Save to Excel", command=self.save).pack(pady=5)
        ttk.Button(self.root, text="Clear Output", command=self.clear_output).pack(pady=5)

    def clear_output(self):
        self.output.delete("1.0", tk.END)

    def generate(self):
        try:
            dish_type = self.dish_type.get()
            source = self.source_selector.get()

            if dish_type == "Dessert/Baking":
                try:
                    self.tray_width = float(self.width_entry.get())
                    self.tray_height = float(self.height_entry.get())
                    tray_size = f"{self.tray_width} x {self.tray_height}"
                except ValueError:
                    messagebox.showerror("Input Error", "Tray size is required for Dessert/Baking.")
                    return
            else:
                self.tray_width = 0
                self.tray_height = 0
                tray_size = None

            selected_dish = discover_dish_name(master_path, dish_type)
            raw_ingredients = get_key_ingredients(master_path)
            key_ingredients = strict_filter_by_dish_type(raw_ingredients, dish_type, master_path)

            if len(key_ingredients) < 3:
                fallback_map = {
                    "Main dish": ["rice", "garam masala", "onion", "tomato"],
                    "Side dish": ["dal", "curd", "vegetables", "papad"],
                    "Dessert/Baking": ["flour", "sugar", "milk", "banana"],
                    "Snacks": ["potato", "bread", "besan", "egg"]
                }
                key_ingredients = fallback_map.get(dish_type, [])

            extra_raw = self.extra_ingredients_entry.get()
            extra_ingredients = [i.strip().lower() for i in extra_raw.split(",") if i.strip()] if extra_raw else []

            snippet_text = f"{selected_dish} is a flavorful dish made with ingredients like {', '.join(key_ingredients[:3])}. Cook the base, add spices, and finish with a garnish."
            verified_context = build_verified_context(snippet_text)
            prompt = build_recipe_prompt(dish_type, key_ingredients, extra_ingredients, tray_size, verified_context)

            if source == "Mistral":
                raw_text = query_mistral(prompt)
                target_path = r"C:\Users\admin\Desktop\Reports\Recipe maker\mistral_generated.xlsx"
            else:
                raw_text = query_gemini(prompt)
                print("🧾 Raw Gemini response:\n", raw_text)
                target_path = r"C:\Users\admin\Desktop\Reports\Recipe maker\gemini_generated.xlsx"

            self.recipe = raw_text

            title, header, ingredients_text, steps_text, self.num_pieces, self.serving_size = parse_gemini_response(
                raw_text)
            self.recipe_title = re.sub(r'[\\/*?:\[\]]', '', header.strip().split("\n")[0])[:31]
            self.recipe_full_title = re.sub(r'[\\/*?:\[\]]', '', header.strip().split("\n")[0])

            def parse_ingredient_line(line):
                line = line.strip()
                if ":" in line:
                    name_raw, qty_raw = line.split(":", 1)
                    name = simplify_name(name_raw)
                    qty_raw = qty_raw.strip().lower()
                    qty_match = re.search(r"[\d.]+", qty_raw)
                    try:
                        qty = float(qty_match.group()) if qty_match else 0.0
                    except ValueError:
                        print(f"❌ Could not convert quantity to float: '{qty_raw}'")
                        qty = 0.0
                    unit_match = re.search(r"(g|ml|pieces?|teaspoon|tablespoon)", qty_raw)
                    unit = unit_match.group() if unit_match else "g"
                    return {"name": name, "qty": qty, "unit": unit}
                return None

            ingredient_lines = [line for line in ingredients_text.split("\n") if line.strip()]
            parsed_ingredients = [parse_ingredient_line(i) for i in ingredient_lines if parse_ingredient_line(i)]

            self.priced_df = price_ingredients(parsed_ingredients, master_path)
            self.cost_summary = calculate_total_cost(self.priced_df, self.num_pieces)

            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, header + "\n")
            self.output.insert(tk.END, f"\n🍴 Yield: {self.num_pieces} servings\n")
            self.output.insert(tk.END, f"⚖️ Serving Size: {self.serving_size}\n")
            self.output.insert(tk.END, "\n🧂 " + ingredients_text + "\n")
            self.output.insert(tk.END, "\n👣 " + steps_text + "\n")

            self.output.insert(tk.END, "\n💰 Ingredient Pricing:\n")
            total_raw_cost = 0
            for _, row in self.priced_df.iterrows():
                name = row["ingredient"]
                qty = row["qty"]
                unit = row["unit"]
                price = row["price_per_unit"]
                total = qty * price
                self.output.insert(tk.END, f"{name} | Qty: {qty:.1f} {unit} | ₹{price:.2f} | ₹{total:.2f}\n")
                total_raw_cost += total

            # ✅ Operational Expense Scaling
            base_labor = 100.0
            base_rent = 100.0
            base_gas = 50.0
            base_electricity = 50.0

            selected_percent = self.operational_var.get().replace("%", "")
            try:
                scale = float(selected_percent) / 100.0
            except ValueError:
                scale = 1.0  # fallback to 100%

            labor = base_labor * scale
            rent = base_rent * scale
            gas = base_gas * scale
            electricity = base_electricity * scale

            total_manufacturing_cost = total_raw_cost + labor + rent + gas + electricity
            profit = 0.25 * total_manufacturing_cost
            selling_price = total_manufacturing_cost + profit

            self.output.insert(tk.END, "\n💰 Cost Summary:\n")
            self.output.insert(tk.END, f"Raw Material Cost: ₹{total_raw_cost:.2f}\n")
            self.output.insert(tk.END, f"Labor: ₹{labor:.2f}\n")
            self.output.insert(tk.END, f"Rent: ₹{rent:.2f}\n")
            self.output.insert(tk.END, f"Gas: ₹{gas:.2f}\n")
            self.output.insert(tk.END, f"Electricity: ₹{electricity:.2f}\n")
            self.output.insert(tk.END, f"📦 Total Manufacturing Cost: ₹{total_manufacturing_cost:.2f}\n")
            self.output.insert(tk.END, f"💰 Profit (25%): ₹{profit:.2f}\n")
            self.output.insert(tk.END, f"🛒 Selling Price: ₹{selling_price:.2f}\n")

            self.target_path = target_path
            self.cost_summary.update({
                "Raw Material Cost": total_raw_cost,
                "Labor": labor,
                "Rent": rent,
                "Gas": gas,
                "Electricity": electricity,
                "Total Manufacturing Cost": total_manufacturing_cost,
                "Profit (25%)": profit,
                "Selling Price": selling_price
            })

        except Exception as e:
            messagebox.showerror("Error", str(e))
            import traceback
            traceback.print_exc()

    def save(self):
        if not self.recipe or self.priced_df is None or self.priced_df.empty:
            messagebox.showerror("Save Error", "No recipe to save.")
            return

        # ✅ Operational Expense Scaling
        base_labor = 100.0
        base_rent = 100.0
        base_gas = 50.0
        base_electricity = 50.0

        selected_percent = self.operational_var.get().replace("%", "")
        try:
            scale = float(selected_percent) / 100.0
        except ValueError:
            scale = 1.0  # fallback to 100% if parsing fails

        self.cost_summary = {
            "labor": base_labor * scale,
            "rent": base_rent * scale,
            "gas": base_gas * scale,
            "electricity": base_electricity * scale
        }

        # ✅ Save to Excel
        log_recipe(
            self.recipe,
            self.priced_df,
            self.target_path,
            self.tray_width,
            self.tray_height,
            self.num_pieces,
            self.serving_size,
            self.cost_summary,
            self.recipe_title  # ✅ Sheet name
        )

        # ✅ Track dish name
        from modules.dish_tracker import ensure_dish_file_exists, save_new_dish
        ensure_dish_file_exists()

        dish_name = self.recipe_full_title.split("Title")[1].strip()
        save_new_dish(dish_name)

        messagebox.showinfo("Saved", f"Recipe saved to {self.target_path}")





if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = RnDBotUI(root)
        root.mainloop()
    except Exception as e:
        print("❌ App crashed:", e)
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")