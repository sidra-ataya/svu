# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Za9yyQ3kV8rwEqbmtOrfIAztmXRlgs5C
"""

import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Define ranges for food type
x_food = np.linspace(0, 100, 100)
raw = fuzz.trimf(x_food, [0, 0, 50])
half_cooked = fuzz.trimf(x_food, [25, 50, 75])
fully_cooked = fuzz.trimf(x_food, [50, 100, 100])

# Define ranges for quantity of food
x_quantity = np.linspace(0, 100, 100)
little = fuzz.trimf(x_quantity, [0, 0, 50])
medium = fuzz.trimf(x_quantity, [25, 50, 75])
large = fuzz.trimf(x_quantity, [50, 100, 100])

# Define ranges for cooking time
x_time = np.linspace(0, 60, 100)  # 0-60 minutes
very_short = fuzz.trimf(x_time, [0, 0, 15])
short = fuzz.trimf(x_time, [0, 15, 30])
medium_time = fuzz.trimf(x_time, [15, 30, 45])
long = fuzz.trimf(x_time, [30, 45, 60])
very_long = fuzz.trimf(x_time, [45, 60, 60])

# Create a new figure for interactive control
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
plt.subplots_adjust(left=0.1, bottom=0.25)

# Plot initial results
ax1.plot(x_food, raw, 'b', label='Raw')
ax1.plot(x_food, half_cooked, 'g', label='Half Cooked')
ax1.plot(x_food, fully_cooked, 'r', label='Fully Cooked')
ax1.set_title('Food Type')
ax1.legend()

ax2.plot(x_quantity, little, 'b', label='Little')
ax2.plot(x_quantity, medium, 'g', label='Medium')
ax2.plot(x_quantity, large, 'r', label='Large')
ax2.set_title('Food Quantity')
ax2.legend()

# Create sliders for values
axfood = plt.axes([0.1, 0.1, 0.65, 0.03])
axquantity = plt.axes([0.1, 0.05, 0.65, 0.03])
sfood = Slider(axfood, 'Food Type', 0, 100, valinit=50)
squantity = Slider(axquantity, 'Quantity', 0, 100, valinit=50)

# Update function
def update(val):
    # Get values from sliders
    food_value = sfood.val
    quantity_value = squantity.val

    # Calculate membership degrees
    food_level_raw = fuzz.interp_membership(x_food, raw, food_value)
    food_level_half = fuzz.interp_membership(x_food, half_cooked, food_value)
    food_level_full = fuzz.interp_membership(x_food, fully_cooked, food_value)

    quantity_level_large = fuzz.interp_membership(x_quantity, large, quantity_value)
    quantity_level_medium = fuzz.interp_membership(x_quantity, medium, quantity_value)
    quantity_level_little = fuzz.interp_membership(x_quantity, little, quantity_value)

    # Define rules
    rule1 = np.fmin(food_level_raw , quantity_level_little)
    time_activation1 = np.fmin(rule1, medium_time)

    rule2 = np.fmin(food_level_raw , quantity_level_medium)
    time_activation2 = np.fmin(rule2, long)

    rule3 = np.fmin(food_level_raw , quantity_level_large)
    time_activation3 = np.fmin(rule3, very_long)

    rule4 = np.fmin(food_level_half , quantity_level_little)
    time_activation4 = np.fmin(rule4 , short)

    rule5 = np.fmin(food_level_half , quantity_level_medium)
    time_activation5 = np.fmin(rule5 , medium_time)

    rule6 = np.fmin(food_level_half, quantity_level_large)
    time_activation6 = np.fmin(rule6, long)

    rule7 = np.fmin(food_level_full, quantity_level_little)
    time_activation7 = np.fmin(rule7, very_short)

    rule8 = np.fmin(food_level_full, quantity_level_medium)
    time_activation8 = np.fmin(rule8, short)

    rule9 = np.fmin(food_level_full , quantity_level_large)
    time_activation9 = np.fmin(rule9 , medium_time)

    # Aggregation of all fuzzy output sets
    aggregated = np.fmax(time_activation1,
                np.fmax(time_activation2,
                np.fmax(time_activation3,
                np.fmax(time_activation4,
                np.fmax(time_activation5,
                np.fmax(time_activation6,
                np.fmax(time_activation7,
                np.fmax(time_activation8,
                time_activation9))))))))

try:
        # Defuzzification (Centroid method)
        cooking_time = fuzz.defuzz(x_time, aggregated, 'centroid')
        if cooking_time is not None:
            print(f"Recommended cooking time: {cooking_time:.2f} minutes")
        else:
            print("Could not determine cooking time")

        # Update the plot
        ax1.clear()
        ax2.clear()

        # Plot initial results
        ax1.plot(x_food, raw, 'b', label='Raw')
        ax1.plot(x_food, half_cooked, 'g', label='Half Cooked')
        ax1.plot(x_food, fully_cooked, 'r', label='Fully Cooked')
        ax1.axvline(food_value, color='k', linestyle='--')
        ax1.set_title('Food Type')
        ax1.legend()

        ax2.plot(x_quantity, little, 'b', label='Little')
        ax2.plot(x_quantity, medium, 'g', label='Medium')
        ax2.plot(x_quantity, large, 'r', label='Large')
        ax2.axvline(quantity_value, color='k', linestyle='--')
        ax2.set_title('Food Quantity')
        ax2.legend()

        fig.canvas.draw_idle()
    except:
        print("Error in defuzzification - try different values")

# Connect update function to sliders
sfood.on_changed(update)
squantity.on_changed(update)

plt.show()