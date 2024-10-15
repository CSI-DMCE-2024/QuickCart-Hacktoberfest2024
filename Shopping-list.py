import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json
import os
import csv

# Global variables
shopping_list = {}
entry_item = None
entry_amount = None
entry_price = None
listbox = None
combobox_category = None
combobox_filter = None
filename = "shopping_list.json"
undo_stack = []
categories = ["Grocery", "Stationery", "Electronics", "Household", "Clothing", "Other", "All"]
is_dark_mode = False

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

# Function to display the shopping list with optional filtering
def display_list(category_filter="All"):
    listbox.delete(0, tk.END)
    for item, details in shopping_list.items():
        amount, price, category = details
        if category_filter == "All" or category_filter == category:
            listbox.insert(tk.END, f"- {item} (Amount: {amount}, Price: ${price:.2f}, Category: {category})")

# Function to add an item to the shopping list
def add_item():
    global entry_item, entry_amount, entry_price, combobox_category
    item = entry_item.get().strip()
    amount = entry_amount.get().strip()
    price = entry_price.get().strip()
    category = combobox_category.get()

    if item and amount and price and category:
        try:
            amount = int(amount)
            price = float(price)
            if amount < 0 or price < 0:
                raise ValueError("Negative values are not allowed.")
            if item in shopping_list:
                shopping_list[item][0] += amount  # Update amount
            else:
                shopping_list[item] = [amount, price, category]  # Store amount, price, and category
            undo_stack.append(('add', item, amount))  # Add action to undo stack
            clear_entries()
            display_list(combobox_filter.get())  # Refresh the list with the current filter
            save_list()  # Save the list after adding
            messagebox.showinfo("Success", f"{amount} {item}(s) at ${price:.2f} each in {category} category have been added to your shopping list.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Please enter item, amount, price, and select a category.")

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
                old_amount = shopping_list[item][0]
                shopping_list[item][0] = new_amount  # Update the item's amount
                undo_stack.append(('edit', item, old_amount))  # Add action to undo stack
                clear_entries()
                display_list(combobox_filter.get())  # Refresh the list with the current filter
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
        undo_stack.append(('remove', item, shopping_list[item]))  # Add action to undo stack
        del shopping_list[item]
        clear_entries()
        display_list(combobox_filter.get())  # Refresh the list with the current filter
        save_list()  # Save the list after removal
        messagebox.showinfo("Success", f"{item} has been removed from your shopping list.")
    else:
        messagebox.showerror("Error", f"{item} is not in your shopping list.")

# Function to undo the last action
def undo_action():
    if undo_stack:
        action, item, data = undo_stack.pop()
        if action == 'add':
            del shopping_list[item]
        elif action == 'edit':
            shopping_list[item][0] = data
        elif action == 'remove':
            shopping_list[item] = data
        display_list(combobox_filter.get())
        save_list()
        messagebox.showinfo("Undo", "Last action has been undone.")
    else:
        messagebox.showerror("Error", "No actions to undo.")

# Function to toggle dark mode
def toggle_dark_mode():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    if is_dark_mode:
        root.configure(bg="#1c1c1c")
        frame.configure(bg="#1c1c1c")
        listbox.configure(bg="#333333", fg="white")
    else:
        root.configure(bg="#2d3250")
        frame.configure(bg="#2d3250")
        listbox.configure(bg="#A0A3B2", fg="black")

# Function to export shopping list as CSV
def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Item", "Amount", "Price", "Category"])
            for item, details in shopping_list.items():
                writer.writerow([item] + details)
        messagebox.showinfo("Export", "Shopping list has been exported as CSV.")

# Function to clear entry fields
def clear_entries():
    entry_item.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    combobox_category.set('')

# Main function to set up the UI
def main():
    global entry_item, entry_amount, entry_price, listbox, combobox_category, combobox_filter, frame, root
    load_list()  # Load the shopping list at startup
    root = tk.Tk()
    root.title("Shopping List")
    root.configure(bg="#2d3250")

    frame = tk.Frame(root, bg="#2d3250")
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    label_item = tk.Label(frame, text="Item:", fg="white", bg="#2d3250", font=("Arial", 12))
    label_item.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    entry_item = tk.Entry(frame, font=("Arial", 12), bg="#4e545f", fg="white")
    entry_item.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    label_amount = tk.Label(frame, text="Amount:", fg="white", bg="#2d3250", font=("Arial", 12))
    label_amount.grid(row=1, column=0, padx=5, pady=5, sticky="e")

    entry_amount = tk.Entry(frame, font=("Arial", 12), bg="#4e545f", fg="white")
    entry_amount.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    label_price = tk.Label(frame, text="Price ($):", fg="white", bg="#2d3250", font=("Arial", 12))
    label_price.grid(row=2, column=0, padx=5, pady=5, sticky="e")

    entry_price = tk.Entry(frame, font=("Arial", 12), bg="#4e545f", fg="white")
    entry_price.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

    # Category dropdown
    label_category = tk.Label(frame, text="Category:", fg="white", bg="#2d3250", font=("Arial", 12))
    label_category.grid(row=3, column=0, padx=5, pady=5, sticky="e")

    combobox_category = ttk.Combobox(frame, values=categories[:-1], font=("Arial", 12))
    combobox_category.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

    # Buttons
    button_add = tk.Button(frame, text="Add", command=add_item, bg="#14a769", fg="white", font=("Arial", 12, "bold"))
    button_add.grid(row=4, column=0, padx=5, pady=10)

    button_edit = tk.Button(frame, text="Edit", command=edit_item, bg="#f39c12", fg="white", font=("Arial", 12, "bold"))
    button_edit.grid(row=4, column=1, padx=5, pady=10)

    button_remove = tk.Button(frame, text="Remove", command=remove_item, bg="#e74c3c", fg="white", font=("Arial", 12, "bold"))
    button_remove.grid(row=5, column=0, padx=5, pady=10)

    button_undo = tk.Button(frame, text="Undo", command=undo_action, bg="#3498db", fg="white", font=("Arial", 12, "bold"))
    button_undo.grid(row=5, column=1, padx=5, pady=10)

    button_csv = tk.Button(frame, text="Export CSV", command=export_to_csv, bg="#8e44ad", fg="white", font=("Arial", 12, "bold"))
    button_csv.grid(row=6, column=0, padx=5, pady=10)

    button_dark_mode = tk.Button(frame, text="Toggle Dark Mode", command=toggle_dark_mode, bg="#34495e", fg="white", font=("Arial", 12, "bold"))
    button_dark_mode.grid(row=6, column=1, padx=5, pady=10)

    # Listbox to display the shopping list
    listbox = tk.Listbox(frame, font=("Arial", 12), bg="#A0A3B2", fg="black")
    listbox.grid(row=0, column=2, rowspan=7, padx=10, pady=5, sticky="nsew")

    # Category filter dropdown
    label_filter = tk.Label(frame, text="Filter by Category:", fg="white", bg="#2d3250", font=("Arial", 12))
    label_filter.grid(row=7, column=0, padx=5, pady=5, sticky="e")

    combobox_filter = ttk.Combobox(frame, values=categories, font=("Arial", 12))
    combobox_filter.grid(row=7, column=1, padx=5, pady=5, sticky="nsew")
    combobox_filter.set("All")
    combobox_filter.bind("<<ComboboxSelected>>", lambda event: display_list(combobox_filter.get()))

    display_list()  # Display the shopping list at startup

    # Set up grid row and column configurations for responsive resizing
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(0, weight=1)

    root.mainloop()

if __name__ == "__main__":
    main()
