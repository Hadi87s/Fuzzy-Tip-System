import math
import tkinter as tk
from tkinter import messagebox


def gaussian_membership(x, mean, sigma):
    """
    Calculate the Gaussian membership degree.
    
    Parameters:
    - x: Crisp input value for the service.
    - mean: Mean value for the Gaussian function.
    - sigma: Standard deviation for the Gaussian function.
    
    Returns:
    - Membership degree.
    """
    return math.exp(-((x - mean) ** 2) / (2 * sigma ** 2))

# Example functions for each service level
def service_poor(x):
    return gaussian_membership(x, mean=2, sigma=1)

def service_good(x):
    return gaussian_membership(x, mean=5, sigma=1.5)

def service_excellent(x):
    return gaussian_membership(x, mean=8, sigma=1)

def rancid(x):
    if 0 < x < 3:
        return 1
    elif 3 < x <= 6:
        return (6 - x) / 3
    elif x > 6:
        return 0

def delicious(x):
    if x < 4:
        return 0
    elif 4 < x <= 7:
        return (x - 4) / 3
    elif x > 7:
        return 1

def fuzzification(service_quality, food_quality):
    rancid_food = rancid(food_quality)
    delicious_food = delicious(food_quality)
    fuzzy_food = {
        "rancid":rancid_food,
        "delicious":delicious_food
    }

    poor_degree = service_poor(service_quality)
    good_degree = service_good(service_quality)
    excellent_degree = service_excellent(service_quality)
    
    fuzzy_service = {
        "poor":poor_degree,
        "good":good_degree,
        "excellent":excellent_degree
    }
    
    return fuzzy_service, fuzzy_food

def apply_rules(fuzzy_service, fuzzy_food):
    cheap_tip = max(fuzzy_service["poor"],fuzzy_food["rancid"])
    average_tip = fuzzy_service["good"]
    generous_tip = max(fuzzy_service["excellent"], fuzzy_food["delicious"])

    # Return a dictionary with fuzzy output values for each tip level
    fuzzy_tip = {
        "cheap": cheap_tip,
        "average": average_tip,
        "generous": generous_tip
    }
    
    return fuzzy_tip

def aggregate(fuzzy_tip):
    return fuzzy_tip  # Consider adding aggregation logic here

def defuzzification(aggregated_tip):
    crisp_tip = 0.0
    for i in range(30):
        if i < 10:
            crisp_tip += aggregated_tip["cheap"] * i
        elif 10 < i < 20:
            crisp_tip += aggregated_tip["average"] * i
        elif 20 < i < 30:
            crisp_tip += aggregated_tip["generous"] * i
            
    total_weight = (10 * aggregated_tip["cheap"]) + (10 * aggregated_tip["average"]) + (10 * aggregated_tip["generous"])
    
    if total_weight > 0:
        crisp_tip /= total_weight  # Normalize by total weight
    else:
        crisp_tip = 0  # Handle the case where there is no weight

    return crisp_tip

def calculate_tip(service_quality, food_quality):
    # Step 1: Fuzzification
    fuzzy_service, fuzzy_food = fuzzification(service_quality, food_quality)

    # Step 2: Rule Evaluation
    fuzzy_tip = apply_rules(fuzzy_service, fuzzy_food)

    # Step 3: Aggregation
    aggregated_tip = aggregate(fuzzy_tip)

    # Step 4: Defuzzification
    crisp_tip = defuzzification(aggregated_tip)
    
    return crisp_tip


def on_calculate():
    # ANSI escape codes
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    BOLD = "\033[1m"
    try:
        service_quality = float(service_entry.get())
        food_quality = float(food_entry.get())
        
        if not (0 <= service_quality <= 10) or not (0 <= food_quality <= 10):
            raise ValueError("Values must be between 0 and 10.")
        
        tip = calculate_tip(service_quality, food_quality)
        print(f"{BLUE}Calculated Tip:{RESET} {BOLD}{RED}{tip}{RESET}")
        result_label.config(text=f"Calculated Tip: {tip:.2f}", fg="#00FF00")  # Bright green text
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Tip Calculator")

# Set the window size and position it in the center of the screen
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# Lock the window size so it cannot be resized
root.resizable(False, False)
root.configure(bg="#23272A")  # Dark background color

# Create and place the labels and entries
tk.Label(root, text="Service Quality (0-10):", bg="#23272A", fg="white").pack(pady=(10, 0))
service_entry = tk.Entry(root, bd=0, bg="#2F3136", fg="white", insertbackground='white', highlightthickness=1, highlightbackground="white")
service_entry.pack(pady=5, padx=20)

tk.Label(root, text="Food Quality (0-10):", bg="#23272A", fg="white").pack(pady=(10, 0))
food_entry = tk.Entry(root, bd=0, bg="#2F3136", fg="white", insertbackground='white', highlightthickness=1, highlightbackground="white")
food_entry.pack(pady=5, padx=20)

# Create a button to calculate the tip with rounded corners
calculate_button = tk.Button(root, text="Calculate Tip", command=on_calculate,
                              bg="#7289DA", fg="white", bd=0, padx=10, pady=5)
calculate_button.pack(pady=20)

# Label to display the result
result_label = tk.Label(root, text="", bg="#23272A", fg="#00FF00", font=("Helvetica", 12, "bold"))
result_label.pack(pady=(10, 0))

# Start the GUI main loop
root.mainloop()