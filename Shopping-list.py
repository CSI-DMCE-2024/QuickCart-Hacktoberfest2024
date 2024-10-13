import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import urllib.parse
import webbrowser  # To open the WhatsApp link in the browser

# Global variables
shopping_list = {}
entry_item = None
entry_amount = None
entry_price = None
tree = None
combobox_category = None
combobox_filter = None

# Path to the JSON file in the same directory as the script
current_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_dir, "shopping_list.json")

categories = ["Grocery", "Stationery", "Electronics", "Household", "Clothing", "Other", "All"]

# Function to load shopping list from a JSON file
def load_list():
    global shopping_list
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            shopping_list = json.load(f)
    else:
        shopping_list = {}  # Initialize an empty dictionary if the file does not exist

# Function to save shopping list to a JSON file
def save_list():
    with open(filename, 'w') as f:
        json.dump(shopping_list, f, indent=4)  # Pretty-print the JSON with indentation

# Function to display the shopping list with optional filtering
def display_list(category_filter="All"):
    for row in tree.get_children():
        tree.delete(row)  # Remove all previous rows
    for item, details in shopping_list.items():
        amount, price, category = details
        if category_filter == "All" or category_filter == category:
            tree.insert("", tk.END, values=(item, amount, f"${price:.2f}", category), iid=item)

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
                shopping_list[item][0] += amount  # Update amount if item already exists
            else:
                shopping_list[item] = [amount, price, category]  # Store amount, price, and category
            clear_entries()
            display_list(combobox_filter.get())  # Refresh the list with the current filter
            save_list()  # Save the list after adding
            messagebox.showinfo("Success", f"{amount} {item}(s) at ${price:.2f} each in {category} category have been added to your shopping list.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Please enter item, amount, price, and select a category.")

# Function to remove an item from the shopping list
def remove_item():
    selected_item = tree.focus()  # Get the selected item
    if selected_item:
        item = tree.item(selected_item)['values'][0]  # Get the item name from the selected row
        if item in shopping_list:
            del shopping_list[item]
            display_list(combobox_filter.get())  # Refresh the list with the current filter
            save_list()  # Save the list after removal
            messagebox.showinfo("Success", f"{item} has been removed from your shopping list.")
        else:
            messagebox.showwarning("Warning", "Item not found.")
    else:
        messagebox.showwarning("Warning", "Please select an item to remove.")

# Function to clear entry fields
def clear_entries():
    entry_item.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    combobox_category.set('')  # Clear category selection

# Function to calculate the total price of all items
def calculate_total():
    total_price = sum(amount * price for amount, price, category in shopping_list.values())
    messagebox.showinfo("Total Price", f"The total price of all items is: ${total_price:.2f}")

# Function to initialize the JSON file and add all items (if not present)
def initialize_json():
    if not os.path.exists(filename):  # If file does not exist, create it and add items
        with open(filename, 'w') as f:
            json.dump(shopping_list, f, indent=4)
        print("Shopping list initialized and saved to a new JSON file.")
    else:
        load_list()  # If the file exists, load the existing data

# Function to clear the entire shopping list and JSON file
def clear_list():
    global shopping_list
    shopping_list = {}  # Clear the global shopping list
    save_list()  # Save the empty list to the JSON file
    display_list()  # Refresh the list view
    messagebox.showinfo("Success", "The shopping list has been cleared.")


# Function to share shopping list on WhatsApp
def share_whatsapp():
    if not shopping_list:
        messagebox.showinfo("Info", "Your shopping list is empty.")
        return
    # Generate the shopping list message with line breaks after each item
    message = "Here's my shopping list:\n"
    for item, (amount, price, category) in shopping_list.items():
        message += f"\nItem: {item}\nAmount: {amount}\nPrice: ${price:.2f}\nCategory: {category}\n"
    
    # URL-encode the message to ensure it appears correctly in WhatsApp
    encoded_message = urllib.parse.quote(message)
    
    # Open WhatsApp share URL
    whatsapp_url = f"https://wa.me/?text={encoded_message}"
    webbrowser.open(whatsapp_url)  # Open the WhatsApp web share link



# Main function to set up the UI
def main():
    global entry_item, entry_amount, entry_price, tree, combobox_category, combobox_filter
    initialize_json()  # Initialize JSON and load the list at startup
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

    # Category dropdown
    label_category = tk.Label(frame, text="Category:", bg="#f0f0f0", font=("Arial", 12))
    label_category.grid(row=3, column=0, padx=5, pady=5, sticky="e")

    combobox_category = ttk.Combobox(frame, values=categories[:-1], font=("Arial", 12), state="readonly")  # Exclude "All"
    combobox_category.grid(row=3, column=1, padx=5, pady=5)

    # Filter dropdown
    label_filter = tk.Label(frame, text="Filter By:", bg="#f0f0f0", font=("Arial", 12))
    label_filter.grid(row=4, column=0, padx=5, pady=5, sticky="e")

    combobox_filter = ttk.Combobox(frame, values=categories, font=("Arial", 12), state="readonly")
    combobox_filter.grid(row=4, column=1, padx=5, pady=5)
    combobox_filter.set("All")  # Default filter is "All"
    combobox_filter.bind("<<ComboboxSelected>>", lambda e: display_list(combobox_filter.get()))

    # Buttons with styles
    button_add = tk.Button(frame, text="Add Item", font=("Arial", 12), bg="#b3ffb3", fg="black", command=add_item)
    button_add.grid(row=5, column=0, padx=5, pady=5, sticky="we")

    button_total = tk.Button(frame, text="Calculate Total", font=("Arial", 12), bg="#b3ffb3", fg="black", command=calculate_total)
    button_total.grid(row=5, column=1, padx=5, pady=5, sticky="we")

    button_clear = tk.Button(frame, text="Clear List", font=("Arial", 12), bg="#ff9999", fg="black", command=clear_list)
    button_clear.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    # WhatsApp share button
    whatsapp_icon = tk.Button(frame, text="Share on WhatsApp", font=("Arial", 12), bg="#00cc44", fg="white", command=share_whatsapp)
    whatsapp_icon.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    # Display the shopping list
    columns = ("Item", "Amount", "Price", "Category")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
    tree.heading("Item", text="Item")
    tree.heading("Amount", text="Amount")
    tree.heading("Price", text="Price")
    tree.heading("Category", text="Category")
    tree.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    button_remove = tk.Button(frame, text="Remove Item", font=("Arial", 12), bg="#ff9999", fg="black", command=remove_item)
    button_remove.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    display_list()  # Display list at startup
    root.mainloop()

if __name__ == "__main__":
    main()
