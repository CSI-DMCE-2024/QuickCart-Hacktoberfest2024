import tkinter as tk
from tkinter import messagebox

# Global variables
shopping_list = {}  # Initialize an empty shopping list
entry_item = None
entry_amount = None
entry_search = None
listbox = None

# Function to display the shopping list
def display_list():
    listbox.delete(0, tk.END)
    for item, amount in shopping_list.items():
        listbox.insert(tk.END, "- " + item + " (Amount: " + str(amount) + ")")

# Function to add an item to the shopping list
def add_item():
    global entry_item, entry_amount
    item = entry_item.get()
    amount = entry_amount.get()
    if item and amount:
        amount = int(amount)
        if item in shopping_list:
            shopping_list[item] += amount
        else:
            shopping_list[item] = amount
        entry_item.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        display_list()
        messagebox.showinfo("Success", str(amount) + " " + item + "(s) have been added to your shopping list.")
    else:
        messagebox.showerror("Error", "Please enter both item and amount.")

# Function to remove an item from the shopping list
def remove_item():
    global entry_item
    item = entry_item.get()
    if item in shopping_list:
        del shopping_list[item]
        entry_item.delete(0, tk.END)
        display_list()
        messagebox.showinfo("Success", item + " has been removed from your shopping list.")
    else:
        messagebox.showerror("Error", item + " is not in your shopping list.")

# Function to calculate the total amount of all items
def calculate_total():
    total = sum(shopping_list.values())
    messagebox.showinfo("Total Items", "Total number of items in the shopping list: " + str(total)) 

def search_item():
    global entry_search
    search = entry_search.get()
    found_search = False
    
    for item in list(shopping_list.keys()):
        print(item)
        if item == search:
            print("found")
            found_search = True
        else: 
            del shopping_list[item]   

    if found_search:
        display_list()
        messagebox.showinfo("Success", " filtered list by " + search + "other entries removed.")
    else:
        print("not found")
        display_list()
        messagebox.showerror("Error", item + " not in your shopping list. All entries removed")

# Main function
def main():
    global entry_item, entry_amount, entry_search, listbox
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

    label_search = tk.Label(frame, text="Search:")
    label_search.grid(row=2, column=0, padx=5, pady=5, sticky="e")

    entry_search = tk.Entry(frame)
    entry_search.grid(row=2, column=1, padx=5, pady=5)

    button_add = tk.Button(frame, text="Add Item", command=add_item)
    button_add.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_remove = tk.Button(frame, text="Remove Item", command=remove_item)
    button_remove.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_display = tk.Button(frame, text="Display List", command=display_list)
    button_display.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_search = tk.Button(frame, text="Display Search", command=search_item)
    button_search.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_calculate = tk.Button(frame, text="Calculate Total", command=calculate_total)
    button_calculate.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    listbox = tk.Listbox(frame)
    listbox.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()
