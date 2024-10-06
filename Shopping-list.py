import tkinter as tk
from tkinter import messagebox

# Global variables
shopping_list = {}  # Initialize an empty shopping list
entry_item = None
entry_amount = None
entry_price = None
entry_search = None
listbox = None

# Function to display the shopping list (filtered or full)
def display_list(filter_text=""):
    listbox.delete(0, tk.END)
    for item, details in shopping_list.items():
        amount, price = details
        if filter_text.lower() in item.lower():
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

# Function to search for items based on user input
def search_item():
    search_text = entry_search.get()  # Get the search query
    display_list(search_text)  # Update the displayed list with the search filter

# Main function
def main():
    global entry_item, entry_amount, entry_price, listbox, entry_search
    root = tk.Tk()
    root.title("Shopping List")
    root.configure(bg="pink")

    frame_logo = tk.Frame(root, bg="#e6ffe6")
    frame_logo.pack(padx=10, pady=10, fill='x')

    label_logo = tk.Label(frame_logo, text="SHOPPING LIST", font=("Helvetica", 24, "bold"), bg="#e6ffe6", fg="#006600")
    label_logo.pack()

    #Main Input Frame
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

    #Buttons with styles
    button_add = tk.Button(frame, text="Add Item", font=("Arial", 12), bg="#b3ffb3", fg="black", command=add_item)
    button_add.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_edit = tk.Button(frame, text="Edit Item", font=("Arial", 12), bg="#ffcc99", fg="black", command=edit_item)
    button_edit.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")  # New Edit button

    button_remove = tk.Button(frame, text="Remove Item", font=("Arial", 12), bg="#ff9999", fg="black", command=remove_item)
    button_remove.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_display = tk.Button(frame, text="Display List", font=("Arial", 12), bg="#cceeff", fg="black", command=display_list)
    button_display.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_calculate = tk.Button(frame, text="Calculate Total Cost", font=("Arial", 12), bg="#ffff99", fg="black", command=calculate_total)
    button_calculate.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_clear = tk.Button(frame, text="Clear List", command=clear_list, font=("Arial", 12), bg="#ffff99", fg="black")
    button_clear.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    # Search Bar
    label_search = tk.Label(frame, text="Search:", bg="#f0f0f0", font=("Arial", 12))
    label_search.grid(row=9, column=0, padx=5, pady=5, sticky="e")

    entry_search = tk.Entry(frame, font=("Arial", 12))
    entry_search.grid(row=9, column=1, padx=5, pady=5)

    button_search = tk.Button(frame, text="Search", font=("Arial", 12), bg="#b3ffb3", fg="black", command=search_item)
    button_search.grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    # Listbox with ScrollBar
    listbox_frame = tk.Frame(frame)
    listbox_frame.grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    listbox = tk.Listbox(listbox_frame, font=("Arial", 12), height=8)
    listbox.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(listbox_frame)
    scrollbar.pack(side="right", fill="y")

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()
