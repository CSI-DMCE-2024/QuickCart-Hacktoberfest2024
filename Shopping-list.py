import tkinter as tk
from tkinter import messagebox
import json
import os

# Global variables
shopping_list = {}  # Initialize an empty shopping list
entry_item = None
entry_amount = None
entry_price = None
listbox = None
FILE_PATH = "shopping_list.json"

# Function to display the shopping list
def display_list():
    listbox.delete(0, tk.END)
    for item, details in shopping_list.items():
        amount, price = details
        listbox.insert(tk.END, f"- {item} (Amount: {amount}, Price: ${price})")

# Function to add an item to the shopping list
def add_item():
    global entry_item, entry_amount, entry_price
    item = entry_item.get()
    amount = entry_amount.get()
    price = entry_price.get()

    if item and amount and price:
        try:
            amount = int(amount)
            price = float(price)
            if item in shopping_list:
                shopping_list[item][0] += amount  # Update amount
            else:
                shopping_list[item] = [amount, price]  # Store amount and price
            entry_item.delete(0, tk.END)
            entry_amount.delete(0, tk.END)
            entry_price.delete(0, tk.END)
            display_list()
            messagebox.showinfo("Success", f"{amount} {item}(s) at ${price} each have been added to your shopping list.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for amount and price.")
    else:
        messagebox.showerror("Error", "Please enter item, amount, and price.")

# Function to remove an item from the shopping list
def remove_item():
    global entry_item
    item = entry_item.get()
    if item in shopping_list:
        del shopping_list[item]
        entry_item.delete(0, tk.END)
        display_list()
        messagebox.showinfo("Success", f"{item} has been removed from your shopping list.")
    else:
        messagebox.showerror("Error", f"{item} is not in your shopping list.")

# Function to edit the amount of an item in the shopping list
def edit_item():
    global entry_item, entry_amount
    item = entry_item.get()
    new_amount = entry_amount.get()

    if item and new_amount:
        try:
            new_amount = int(new_amount)
            if item in shopping_list:
                shopping_list[item][0] = new_amount  # Update the item's amount
                entry_item.delete(0, tk.END)
                entry_amount.delete(0, tk.END)
                display_list()
                messagebox.showinfo("Success", f"The amount of {item} has been updated to {new_amount}.")
            else:
                messagebox.showerror("Error", f"{item} is not in your shopping list.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the amount.")
    else:
        messagebox.showerror("Error", "Please enter both item and new amount.")

# Function to clear the entire shopping list
def clear_list():
    global shopping_list
    shopping_list.clear()
    display_list()
    messagebox.showinfo("Success", "All items have been cleared from your shopping list.")        

# Function to calculate the total cost of all items
def calculate_total():
    total = sum(amount * price for amount, price in shopping_list.values())
    messagebox.showinfo("Total Cost", f"Total cost of items in the shopping list: ${total:.2f}")

# Function to save the shopping list to a file
def save_list_to_file():
    with open(FILE_PATH, 'w') as file:
        json.dump(shopping_list, file)

# Function to load the shopping list from a file
def load_list_from_file():
    global shopping_list
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            shopping_list = json.load(file)
        display_list()

# Main function
def main():
    global entry_item, entry_amount, entry_price, listbox
    root = tk.Tk()
    root.title("Shopping List")

    frame_logo = tk.Frame(root)
    frame_logo.pack(padx=10, pady=10)

    label_logo = tk.Label(frame_logo, text="SHOPPING LIST", font=("Helvetica", 24, "bold"))
    label_logo.pack()

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    label_item = tk.Label(frame, text="Item:")
    label_item.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    entry_item = tk.Entry(frame)
    entry_item.grid(row=0, column=1, padx=5, pady=5)

    label_amount = tk.Label(frame, text="Amount:")
    label_amount.grid(row=1, column=0, padx=5, pady=5, sticky="e")

    entry_amount = tk.Entry(frame)
    entry_amount.grid(row=1, column=1, padx=5, pady=5)

    label_price = tk.Label(frame, text="Price ($):")
    label_price.grid(row=2, column=0, padx=5, pady=5, sticky="e")

    entry_price = tk.Entry(frame)
    entry_price.grid(row=2, column=1, padx=5, pady=5)

    button_add = tk.Button(frame, text="Add Item", command=add_item)
    button_add.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_edit = tk.Button(frame, text="Edit Item", command=edit_item)
    button_edit.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_remove = tk.Button(frame, text="Remove Item", command=remove_item)
    button_remove.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_display = tk.Button(frame, text="Display List", command=display_list)
    button_display.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_calculate = tk.Button(frame, text="Calculate Total Cost", command=calculate_total)
    button_calculate.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_clear = tk.Button(frame, text="Clear List", command=clear_list)
    button_clear.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    listbox = tk.Listbox(frame)
    listbox.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    # Load the shopping list from the file
    load_list_from_file()

    # Save the shopping list to the file when the window is closed
    root.protocol("WM_DELETE_WINDOW", lambda: [save_list_to_file(), root.destroy()])

    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()
