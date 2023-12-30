import tkinter as tk
from tkinter import ttk

# Function to update units based on the slider position
def update_units(event=None):
    if unit_scale.get() == 0:  # Metric units
        height_label.config(text="Height (cm):")
        weight_label.config(text="Weight (kg):")
        feet_entry.grid_remove()
        inches_entry.grid_remove()
        height_entry.grid()
    else:  # Wrong units
        height_label.config(text="Height:")
        weight_label.config(text="Weight (lbs):")
        feet_entry.grid()
        inches_entry.grid()
        height_entry.grid_remove()

# Function to calculate macros
def calculate_macros():
    try:
        # Converting input to Metric if using "Wrong" (Imperial) units
        if unit_scale.get() == 1:
            feet = int(feet_entry.get())
            inches = int(inches_entry.get())
            height = (feet * 12 + inches) * 2.54  # feet and inches to cm
            weight = int(weight_entry.get()) * 0.453592  # lbs to kg
        else:
            height = int(height_entry.get())
            weight = int(weight_entry.get())

        age = int(age_entry.get())
        gender = gender_var.get()
        activity_level = activity_var.get()
        goal = goal_var.get()

        # Basic BMR Calculation
        if gender == "Male":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

        # Adjusting BMR based on activity level
        activity_factor = {"Sedentary": 1.2, "Lightly active": 1.375,
                           "Moderately active": 1.55, "Very active": 1.725}
        tdee = bmr * activity_factor[activity_level]

        # Adjusting TDEE based on goal
        if goal == "Lose weight":
            tdee -= 500  # Creating a caloric deficit
        elif goal == "Gain muscle":
            tdee += 500  # Creating a caloric surplus

        # Calculating Macros
        carbs = (tdee * 0.4) / 4  # 4 calories per gram
        protein = (tdee * 0.3) / 4
        fats = (tdee * 0.3) / 9  # 9 calories per gram

        # Displaying the results
        result_label.config(text=f"Carbs: {carbs:.0f}g, Protein: {protein:.0f}g, Fats: {fats:.0f}g")
    except ValueError:
        result_label.config(text="Please enter valid numbers.")

# Setting up the main window
root = tk.Tk()
root.title("Macro Calculator")

# Defining the Tkinter variables
gender_var = tk.StringVar(value="Male")
activity_var = tk.StringVar(value="Sedentary")
goal_var = tk.StringVar(value="Maintain weight")

# Creating the UI elements
age_label = tk.Label(root, text="Age:")
age_entry = tk.Entry(root)

height_label = tk.Label(root, text="Height (cm):")
height_entry = tk.Entry(root)  # Used for metric system
feet_entry = tk.Entry(root, width=5)  # Used for imperial system (feet)
inches_entry = tk.Entry(root, width=5)  # Used for imperial system (inches)

weight_label = tk.Label(root, text="Weight (kg):")
weight_entry = tk.Entry(root)

gender_label = tk.Label(root, text="Gender:")
gender_dropdown = ttk.Combobox(root, textvariable=gender_var, values=["Male", "Female"])

activity_label = tk.Label(root, text="Activity Level:")
activity_dropdown = ttk.Combobox(root, textvariable=activity_var, 
                                 values=["Sedentary", "Lightly active", "Moderately active", "Very active"])

goal_label = tk.Label(root, text="Goal:")
goal_dropdown = ttk.Combobox(root, textvariable=goal_var, 
                             values=["Lose weight", "Maintain weight", "Gain muscle"])

unit_label = tk.Label(root, text="Unit System:")
unit_scale = tk.Scale(root, from_=0, to=1, orient=tk.HORIZONTAL, showvalue=0, command=update_units)
unit_scale.set(0)  # Default to Metric units

calculate_button = tk.Button(root, text="Calculate Macros", command=calculate_macros)
result_label = tk.Label(root, text="")

# Placing the UI elements on the window
age_label.grid(row=0, column=0)
age_entry.grid(row=0, column=1)

height_label.grid(row=1, column=0)
height_entry.grid(row=1, column=1)
feet_entry.grid(row=1, column=1, sticky="w")
inches_entry.grid(row=1, column=1, sticky="e")
feet_entry.grid_remove()  # Hide feet and inches entry by default
inches_entry.grid_remove()  # Hide feet and inches entry by default

weight_label.grid(row=2, column=0)
weight_entry.grid(row=2, column=1)

gender_label.grid(row=3, column=0)
gender_dropdown.grid(row=3, column=1)

activity_label.grid(row=4, column=0)
activity_dropdown.grid(row=4, column=1)

goal_label.grid(row=5, column=0)
goal_dropdown.grid(row=5, column=1)

unit_label.grid(row=6, column=0)
unit_scale.grid(row=6, column=1)

calculate_button.grid(row=7, column=0, columnspan=2)
result_label.grid(row=8, column=0, columnspan=2)

# Running the application
root.mainloop()