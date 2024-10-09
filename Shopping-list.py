import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from PIL import Image, ImageTk, ImageDraw

# Global variables
shopping_list = {}
entry_item = None
entry_amount = None
entry_price = None
listbox = None
combobox_category = None
combobox_filter = None
filename = "shopping_list.json"
categories = ["Grocery", "Stationery", "Electronics", "Household", "Clothing", "Other", "All"]

# Function to create a rounded button image
def create_rounded_button(width, height, radius, color):
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(image)
    
    # Draw rounded rectangle
    draw.rounded_rectangle((0, 0, width, height), radius, fill=color)
    
    return ImageTk.PhotoImage(image)

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
                shopping_list[item][0] = new_amount  # Update the item's amount
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
        del shopping_list[item]
        clear_entries()
        display_list(combobox_filter.get())  # Refresh the list with the current filter
        save_list()  # Save the list after removal
        messagebox.showinfo("Success", f"{item} has been removed from your shopping list.")
    else:
        messagebox.showerror("Error", f"{item} is not in your shopping list.")

# Function to clear the entire shopping list
def clear_list():
    global shopping_list
    shopping_list.clear()
    display_list()  # Clear display
    save_list()  # Save the cleared list
    messagebox.showinfo("Success", "All items have been cleared from your shopping list.")

# Function to calculate the total cost of all items
def calculate_total():
    total = sum(amount * price for amount, price, _ in shopping_list.values())
    messagebox.showinfo("Total Cost", f"Total cost of items in the shopping list: ${total:.2f}")

# Function to search for an item in the shopping list
def search_item():
    global entry_item
    search_term = entry_item.get().strip().lower()
    listbox.delete(0, tk.END)
    found = False
    for item, details in shopping_list.items():
        if search_term in item.lower():
            amount, price, category = details
            listbox.insert(tk.END, f"- {item} (Amount: {amount}, Price: ${price:.2f}, Category: {category})")
            found = True
    if not found:
        messagebox.showinfo("Search Result", "No matching items found.")

# Function to filter items by category
def filter_items():
    display_list(combobox_filter.get())

# Function to clear entry fields
def clear_entries():
    entry_item.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    combobox_category.set('')  # Clear category selection

# Function to set up custom buttons with rounded edges and blue-beige theme
def create_custom_button(frame, text, command, row, column, padx=5, pady=5, width=200, height=50, radius=25, columnspan=1):
    # Create rounded button image in blue
    button_image = create_rounded_button(width, height, radius, "#005f99")  # Blue color
    
    button = tk.Button(frame, text=text, command=command, image=button_image, compound="center", font=("Arial", 12, "bold"), fg="beige", bg="beige", borderwidth=0)
    button.image = button_image  # Keep reference to the image
    button.grid(row=row, column=column, padx=padx, pady=pady, sticky="we", columnspan=columnspan)

# Main function to set up the UI
def main():
    global entry_item, entry_amount, entry_price, listbox, combobox_category, combobox_filter
    load_list()  # Load the shopping list at startup
    root = tk.Tk()
    root.title("Shopping List")
    root.configure(bg="beige")

    # Logo
    frame_logo = tk.Frame(root, bg="beige")
    frame_logo.pack(padx=10, pady=10, fill='x')

    label_logo = tk.Label(frame_logo, text="SHOPPING LIST", font=("Helvetica", 24, "bold"), bg="beige", fg="#005f99")
    label_logo.pack()

    # Main Input Frame
    frame = tk.Frame(root, bg="beige")
    frame.pack(padx=10, pady=10, fill='both', expand=True)

    label_item = tk.Label(frame, text="Item:", bg="beige", fg="blue", font=("Arial", 12))
    label_item.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    entry_item = tk.Entry(frame, font=("Arial", 12), bg="white", fg="black")
    entry_item.grid(row=0, column=1, padx=5, pady=5)

    label_amount = tk.Label(frame, text="Amount:", bg="beige", fg="blue", font=("Arial", 12))
    label_amount.grid(row=1, column=0, padx=5, pady=5, sticky="e")

    entry_amount = tk.Entry(frame, font=("Arial", 12), bg="white", fg="black")
    entry_amount.grid(row=1, column=1, padx=5, pady=5)

    label_price = tk.Label(frame, text="Price ($):", bg="beige", fg="blue", font=("Arial", 12))
    label_price.grid(row=2, column=0, padx=5, pady=5, sticky="e")

    entry_price = tk.Entry(frame, font=("Arial", 12), bg="white", fg="black")
    entry_price.grid(row=2, column=1, padx=5, pady=5)

    # Category dropdown
    label_category = tk.Label(frame, text="Category:", bg="beige", fg="blue", font=("Arial", 12))
    label_category.grid(row=3, column=0, padx=5, pady=5, sticky="e")

    combobox_category = ttk.Combobox(frame, values=categories[:-1], font=("Arial", 12), state="readonly")
    combobox_category.grid(row=3, column=1, padx=5, pady=5)

    # Filter dropdown
    label_filter = tk.Label(frame, text="Filter By:", bg="beige", fg="blue", font=("Arial", 12))
    label_filter.grid(row=4, column=0, padx=5, pady=5, sticky="e")

    combobox_filter = ttk.Combobox(frame, values=categories, font=("Arial", 12), state="readonly")
    combobox_filter.grid(row=4, column=1, padx=5, pady=5)
    combobox_filter.set("All")
    combobox_filter.bind("<<ComboboxSelected>>", lambda e: filter_items())

    # Create buttons
    create_custom_button(frame, "Add Item", add_item, row=5, column=0)
    create_custom_button(frame, "Edit Item", edit_item, row=5, column=1)
    create_custom_button(frame, "Remove Item", remove_item, row=6, column=0)
    create_custom_button(frame, "Display List", lambda: display_list(combobox_filter.get()), row=6, column=1)
    create_custom_button(frame, "Search Item", search_item, row=7, column=0)
    create_custom_button(frame, "Calculate Total", calculate_total, row=7, column=1)
    create_custom_button(frame, "Clear List", clear_list, row=8, column=0, columnspan=2)

    # Listbox to display the items
    listbox_frame = tk.Frame(root)
    listbox_frame.pack(padx=10, pady=10, fill='both', expand=True)

    listbox = tk.Listbox(listbox_frame, font=("Arial", 12), width=50, height=10)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(listbox_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    display_list()  # Initial display of the shopping list
    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()
