import tkinter as tk
from tkinter import messagebox
import json
import os

# Global variables
shopping_list = {}
entry_item = None
entry_amount = None
entry_price = None
listbox = None
filename = "shopping_list.json"

# Function to load shopping list from a JSON file
def load_list():
    global shopping_list
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            shopping_list = json.load(f)

# Function to save shopping list to a JSON file
def save_list():
    with open(filename, 'w') as f:
        json.dump(shopping_list, f)

# Function to display the shopping list
def display_list():
    listbox.delete(0, tk.END)
    for item, details in shopping_list.items():
        amount, price = details
        listbox.insert(tk.END, f"- {item} (Amount: {amount}, Price: ${price:.2f})")

# Function to add an item to the shopping list
def add_item():
    global entry_item, entry_amount, entry_price
    item = entry_item.get().strip()
    amount = entry_amount.get().strip()
    price = entry_price.get().strip()
    
    if item and amount and price:
        try:
            amount = int(amount)
            price = float(price)
            if amount < 0 or price < 0:
                raise ValueError("Negative values are not allowed.")
            if item in shopping_list:
                shopping_list[item][0] += amount  # Update amount
            else:
                shopping_list[item] = [amount, price]  # Store amount and price
            clear_entries()
            display_list()
            save_list()  # Save the list after adding
            messagebox.showinfo("Success", f"{amount} {item}(s) at ${price:.2f} each have been added to your shopping list.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Please enter item, amount, and price.")

# Function to edit the amount of an item in the shopping list
def edit_item():
    global entry_item, entry_amount
    item = entry_item.get().strip()
    new_amount = entry_amount.get().strip()
    
    if item and new_amount:
        try:
            new_amount = int(new_amount)
            if new_amount < 0:
                raise ValueError("Negative values are not allowed.")
            if item in shopping_list:
                shopping_list[item][0] = new_amount  # Update the item's amount
                clear_entries()
                display_list()
                save_list()  # Save the list after editing
                messagebox.showinfo("Success", f"The amount of {item} has been updated to {new_amount}.")
            else:
                messagebox.showerror("Error", f"{item} is not in your shopping list.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Please enter both item and new amount.")

# Function to remove an item from the shopping list
def remove_item():
    global entry_item
    item = entry_item.get().strip()
    if item in shopping_list:
        del shopping_list[item]
        clear_entries()
        display_list()
        save_list()  # Save the list after removal
        messagebox.showinfo("Success", f"{item} has been removed from your shopping list.")
    else:
        messagebox.showerror("Error", f"{item} is not in your shopping list.")

# Function to clear the entire shopping list
def clear_list():
    global shopping_list
    shopping_list.clear()
    display_list()
    save_list()  # Save the cleared list
    messagebox.showinfo("Success", "All items have been cleared from your shopping list.")

# Function to calculate the total cost of all items
def calculate_total():
    total = sum(amount * price for amount, price in shopping_list.values())
    messagebox.showinfo("Total Cost", f"Total cost of items in the shopping list: ${total:.2f}")

# Function to search for an item in the shopping list
def search_item():
    global entry_item
    search_term = entry_item.get().strip().lower()
    listbox.delete(0, tk.END)
    found = False
    for item, details in shopping_list.items():
        if search_term in item.lower():
            amount, price = details
            listbox.insert(tk.END, f"- {item} (Amount: {amount}, Price: ${price:.2f})")
            found = True
    if not found:
        messagebox.showinfo("Search Result", "No matching items found.")

# Function to clear entry fields
def clear_entries():
    entry_item.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_price.delete(0, tk.END)

# Main function to set up the UI
def main():
    global entry_item, entry_amount, entry_price, listbox
    load_list()  # Load the shopping list at startup
    root = tk.Tk()
    root.title("Shopping List")
    root.configure(bg="pink")

    frame_logo = tk.Frame(root, bg="#e6ffe6")
    frame_logo.pack(padx=10, pady=10, fill='x')

    label_logo = tk.Label(frame_logo, text="SHOPPING LIST", font=("Helvetica", 24, "bold"), bg="#e6ffe6", fg="#006600")
    label_logo.pack()

    # Main Input Frame
    frame = tk.Frame(root, bg="#007FFF")
    frame.pack(padx=10, pady=10, fill='both', expand=True)

    label_item = tk.Label(frame, text="Item:", bg="#f0f0f0", font=("Arial", 12))
    label_item.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    entry_item = tk.Entry(frame, font=("Arial", 12))
    entry_item.grid(row=0, column=1, padx=5, pady=5)

    label_amount = tk.Label(frame, text="Amount:", bg="#f0f0f0", font=("Arial", 12))
    label_amount.grid(row=1, column=0, padx=5, pady=5, sticky="e")

    entry_amount = tk.Entry(frame, font=("Arial", 12))
    entry_amount.grid(row=1, column=1, padx=5, pady=5)

    label_price = tk.Label(frame, text="Price ($):", bg="#f0f0f0", font=("Arial", 12))
    label_price.grid(row=2, column=0, padx=5, pady=5, sticky="e")

    entry_price = tk.Entry(frame, font=("Arial", 12))
    entry_price.grid(row=2, column=1, padx=5, pady=5)

    # Buttons with styles
    button_frame = tk.Frame(frame, bg="#007FFF")
    button_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_add = tk.Button(button_frame, text="Add Item", font=("Arial", 12), bg="#b3ffb3", fg="black", command=add_item)
    button_add.grid(row=0, column=0, padx=5, pady=5, sticky="we")

    button_edit = tk.Button(button_frame, text="Edit Item", font=("Arial", 12), bg="#ffcc99", fg="black", command=edit_item)
    button_edit.grid(row=0, column=1, padx=5, pady=5, sticky="we")

    button_remove = tk.Button(button_frame, text="Remove Item", font=("Arial", 12), bg="#ff9999", fg="black", command=remove_item)
    button_remove.grid(row=1, column=0, padx=5, pady=5, sticky="we")

    button_display = tk.Button(button_frame, text="Display List", font=("Arial", 12), bg="#cceeff", fg="black", command=display_list)
    button_display.grid(row=1, column=1, padx=5, pady=5, sticky="we")

    button_search = tk.Button(button_frame, text="Search Item", font=("Arial", 12), bg="#ccffcc", fg="black", command=search_item)
    button_search.grid(row=2, column=0, padx=5, pady=5, sticky="we")

    button_calculate = tk.Button(button_frame, text="Calculate Total Cost", font=("Arial", 12), bg="#ffff99", fg="black", command=calculate_total)
    button_calculate.grid(row=2, column=1, padx=5, pady=5, sticky="we")

    button_clear = tk.Button(button_frame, text="Clear List", font=("Arial", 12), bg="#ffccff", fg="black", command=clear_list)
    button_clear.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    # Listbox to display the items
    listbox_frame = tk.Frame(root)
    listbox_frame.pack(padx=10, pady=10, fill='both', expand=True)

    listbox = tk.Listbox(listbox_frame, font=("Arial", 12), width=50, height=15)
    listbox.pack(padx=5, pady=5, fill='both', expand=True)

    # Scrollbar for the listbox
    scrollbar = tk.Scrollbar(listbox_frame, orient="vertical", command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)

    root.mainloop()

if __name__ == "__main__":
    main()
