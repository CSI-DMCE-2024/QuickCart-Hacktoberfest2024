import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # Import ttk for Treeview

# Global shopping list dictionary
shopping_list = {}

# Function to display the shopping list in the Treeview
def display_list(treeview):
    # Clear the Treeview before inserting new items
    for item in treeview.get_children():
        treeview.delete(item)

    # Insert items into the Treeview
    for item, amount in shopping_list.items():
        treeview.insert("", "end", values=(item, amount))

# Function to add an item to the shopping list
def add_item(entry_item, entry_amount, treeview):
    item = entry_item.get().strip()
    amount = entry_amount.get().strip()

    if item and amount:
        try:
            amount = int(amount)
            if item in shopping_list:
                shopping_list[item] += amount
            else:
                shopping_list[item] = amount
            entry_item.delete(0, tk.END)
            entry_amount.delete(0, tk.END)
            display_list(treeview)
            messagebox.showinfo("Success", f"{amount} {item}(s) have been added to your shopping list.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the amount.")
    else:
        messagebox.showerror("Error", "Please enter both item and amount.")

# Function to remove an item from the shopping list
def remove_item(entry_item, treeview):
    item = entry_item.get().strip()
    if item in shopping_list:
        del shopping_list[item]
        entry_item.delete(0, tk.END)
        display_list(treeview)
        messagebox.showinfo("Success", f"{item} has been removed from your shopping list.")
    else:
        messagebox.showerror("Error", f"{item} is not in your shopping list.")

# Function to calculate the total amount of items in the shopping list
def calculate_total():
    total = sum(shopping_list.values())
    messagebox.showinfo("Total Items", f"Total number of items in the shopping list: {total}")

# Main function to create the GUI
def main():
    root = tk.Tk()
    root.title("Shopping List")

    # Logo frame
    frame_logo = tk.Frame(root)
    frame_logo.pack(padx=10, pady=10)

    label_logo = tk.Label(frame_logo, text="SHOPPING LIST", font=("Helvetica", 24, "bold"))
    label_logo.pack()

    # Main frame
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    # Item label and entry
    label_item = tk.Label(frame, text="Item:")
    label_item.grid(row=0, column=0, padx=5, pady=5, sticky="e")

    entry_item = tk.Entry(frame)
    entry_item.grid(row=0, column=1, padx=5, pady=5)

    # Amount label and entry
    label_amount = tk.Label(frame, text="Amount:")
    label_amount.grid(row=1, column=0, padx=5, pady=5, sticky="e")

    entry_amount = tk.Entry(frame)
    entry_amount.grid(row=1, column=1, padx=5, pady=5)

    # Buttons for adding, removing, displaying, and calculating
    button_add = tk.Button(frame, text="Add Item", command=lambda: add_item(entry_item, entry_amount, treeview))
    button_add.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_remove = tk.Button(frame, text="Remove Item", command=lambda: remove_item(entry_item, treeview))
    button_remove.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    button_calculate = tk.Button(frame, text="Calculate Total", command=calculate_total)
    button_calculate.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="we")

    # Treeview to display the shopping list with two columns: Item and Amount
    treeview = ttk.Treeview(frame, columns=("Item", "Amount"), show="headings", height=8)
    treeview.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

    # Configure column headers
    treeview.heading("Item", text="Item")
    treeview.heading("Amount", text="Amount")
    treeview.column("Item", anchor="w", width=150)
    treeview.column("Amount", anchor="center", width=100)

    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()
