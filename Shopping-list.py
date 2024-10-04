import tkinter as tk
from tkinter import messagebox, filedialog

# Global variables
shopping_list = {}  # Initialize an empty shopping list
entry_item = None
entry_amount = None
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

# New Feature: Edit the quantity of an existing item
def edit_item():
    global entry_item, entry_amount
    item = entry_item.get()
    amount = entry_amount.get()
    if item in shopping_list:
        if amount.isdigit():
            shopping_list[item] = int(amount)
            display_list()
            messagebox.showinfo("Success", f"{item}'s amount has been updated to {amount}.")
        else:
            messagebox.showerror("Error", "Please enter a valid amount.")
    else:
        messagebox.showerror("Error", item + " is not in your shopping list.")

# New Feature: Save the shopping list to a text file
def save_list():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            for item, amount in shopping_list.items():
                file.write(f"{item}: {amount}\n")
        messagebox.showinfo("Success", "Shopping list has been saved.")

# New Feature: Load the shopping list from a text file
def load_list():
    global shopping_list
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            shopping_list.clear()
            for line in file:
                item, amount = line.strip().split(": ")
                shopping_list[item] = int(amount)
        display_list()
        messagebox.showinfo("Success", "Shopping list has been loaded.")

# New Feature: Clear the shopping list
def clear_list():
    global shopping_list
    shopping_list.clear()
    display_list()
    messagebox.showinfo("Success", "Shopping list has been cleared.")

# Main function
def main():
    global entry_item, entry_amount, listbox
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

    button_add = tk.Button(frame, text="Add Item", command=add_item)
    button_add.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_remove = tk.Button(frame, text="Remove Item", command=remove_item)
    button_remove.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_edit = tk.Button(frame, text="Edit Item", command=edit_item)
    button_edit.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_display = tk.Button(frame, text="Display List", command=display_list)
    button_display.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_calculate = tk.Button(frame, text="Calculate Total", command=calculate_total)
    button_calculate.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_clear = tk.Button(frame, text="Clear List", command=clear_list)
    button_clear.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_save = tk.Button(frame, text="Save List", command=save_list)
    button_save.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_load = tk.Button(frame, text="Load List", command=load_list)
    button_load.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    listbox = tk.Listbox(frame)
    listbox.grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()