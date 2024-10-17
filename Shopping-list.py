import tkinter as tk
from tkinter import messagebox, ttk
import json
import os


shopping_list = {} 

filename = "shopping_list.json"
categories = ["Grocery", "Stationery", "Electronics", "Household", "Clothing", "Other", "All"]

def load_list():
    global shopping_list
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            shopping_list = json.load(f)

#save list in json file
def save_list():
    with open(filename, 'w') as f:
        json.dump(shopping_list, f)



def display_list(category_filter="All"):
    listbox.delete(0, tk.END)
    for item, details in shopping_list.items():
        amount, price, category, checked = details
        if category_filter == "All" or category_filter == category:
            checkmark = "✔" if checked else "✘"
            listbox.insert(tk.END, f"{checkmark} - {item} (Amount: {amount}, Price: ${price:.2f}, Category: {category})")

def toggle_item(event):
    index = listbox.curselection()
    if index:
        item = listbox.get(index[0]).split(" - ")[1].split(" (")[0]  
        if item in shopping_list:
            shopping_list[item][3] = not shopping_list[item][3]  # Toggle checked status
            save_list()  # Save changes
            display_list(combobox_filter.get())  # 




#  add item to the shopping list
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

                shopping_list[item] = [amount, price , category , False]  # Store amount and price 
            clear_entries()
            display_list(combobox_filter.get())
            save_list() 
            
          
            messagebox.showinfo("Success", f"{amount} {item}(s) at ${price:.2f} each have added to your shopping list.")
        except ValueError:
            messagebox.showerror("Error", "enter valid numbers for amount and price.")
    else:
        messagebox.showerror("Error", "Please enter item, amount, and price.")

# remove item from the shopping list
def remove_item():
    global entry_item
    item = entry_item.get().strip()
    if item in shopping_list:
        del shopping_list[item]
        clear_entries()
        display_list(combobox_filter.get())  # Refresh the list with the current filter
        save_list()  
        messagebox.showinfo("Success", f"{item} has been removed from your shopping list.")
    else:
        messagebox.showerror("Error", f"{item} is not in your shopping list.")
    
def clear_list():
    global shopping_list
    shopping_list.clear()
    display_list()  # Clear display
    save_list()  # Save the cleared list
    messagebox.showinfo("Success", "All items have been cleared from your shopping list.")

# Function to calculate the total cost of all items
def calculate_total():
    total = sum(amount * price for amount, price, _, _ in shopping_list.values())
    messagebox.showinfo("Total Cost", f"Total cost of items in the shopping list: ${total:.2f}")

# Function to filter items by category
def filter_items():
    display_list(combobox_filter.get())

# Function to clear entry fields
def clear_entries():
    entry_item.delete(0, tk.END)
    entry_amount.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    combobox_category.set('')  # Clear category selection

# Main function to set up the UI
def main():
    global entry_item, entry_amount, entry_price, listbox, combobox_category, combobox_filter
    load_list()  # Load the shopping list at startup
    root = tk.Tk()
    root.title("Shopping List")
    root.configure(bg="#2d3250")

    # Main Input Frame
    frame = tk.Frame(root, bg="#4e545f")
    frame.pack(padx=10, pady=10, fill='both', expand=True)

    # Input fields
    label_item = tk.Label(frame, text="Item:", bg="#4e545f", fg="#ffffff", font=("Arial", 12))
    label_item.grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_item = tk.Entry(frame, font=("Arial", 12))
    entry_item.grid(row=0, column=1, padx=5, pady=5)

    label_amount = tk.Label(frame, text="Amount:", bg="#4e545f", font=("Arial", 12))
    label_amount.grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_amount = tk.Entry(frame, font=("Arial", 12))
    entry_amount.grid(row=1, column=1, padx=5, pady=5)

    label_price = tk.Label(frame, text="Price ($):", bg="#4e545f", fg="#ffffff", font=("Arial", 12))
    label_price.grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_price = tk.Entry(frame, font=("Arial", 12))
    entry_price.grid(row=2, column=1, padx=5, pady=5)

    # Buttons
    button_add = tk.Button(frame, text="Add Item", font=("Arial", 12), bg="#FF7F50", fg="white", command=add_item)
    button_add.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")
    
    button_remove = tk.Button(frame, text="Remove Item", font=("Arial", 12), bg="#FF7F50", fg="white", command=remove_item)
    button_remove.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_calculate = tk.Button(frame, text="Calculate Total Cost", font=("Arial", 12), bg="#FF7F50", fg="white", command=calculate_total)
    button_calculate.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    # Category dropdown
    label_category = tk.Label(frame, text="Category:", bg="#f0f0f0", font=("Arial", 12))
    label_category.grid(row=6, column=0, padx=5, pady=5, sticky="e")
    combobox_category = ttk.Combobox(frame, values=categories[:-1], font=("Arial", 12), state="readonly")  # Exclude "All"
    combobox_category.grid(row=6, column=1, padx=5, pady=5)

    # Filter dropdown
    label_filter = tk.Label(frame, text="Filter By:", bg="#f0f0f0", font=("Arial", 12))
    label_filter.grid(row=7, column=0, padx=5, pady=5, sticky="e")
    combobox_filter = ttk.Combobox(frame, values=categories, font=("Arial", 12), state="readonly")
    combobox_filter.grid(row=7, column=1, padx=5, pady=5)
    combobox_filter.set("All")  # Default filter is "All"
    combobox_filter.bind("<<ComboboxSelected>>", lambda e: filter_items())

    # Listbox to display the items
    listbox_frame = tk.Frame(root)
    listbox_frame.pack(padx=10, pady=10, fill='both', expand=True)

    listbox = tk.Listbox(listbox_frame, font=("Arial", 12), width=50, height=10)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(listbox_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    listbox.bind("<Double-Button-1>", toggle_item)  # Bind double click to toggle item

    display_list()  # Initial display of the shopping list

    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()


    

 



    



