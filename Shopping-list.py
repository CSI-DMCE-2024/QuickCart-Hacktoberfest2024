import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style

# Global variables
shopping_list = {}  # Initialize an empty shopping list
entry_item = None
entry_amount = None
listbox = None

# Function to display the shopping list
def display_list():
    listbox.delete(0, tk.END)
    for item, amount in shopping_list.items():
        listbox.insert(tk.END, f"{item} (Amount: {amount})")

# Function to add an item to the shopping list
def add_item():
    global entry_item, entry_amount
    item = entry_item.get()
    amount = entry_amount.get()
    if item and amount:
        try:
            amount = int(amount)
            if item in shopping_list:
                shopping_list[item] += amount
            else:
                shopping_list[item] = amount
            entry_item.delete(0, tk.END)
            entry_amount.delete(0, tk.END)
            display_list()
            messagebox.showinfo("Success", f"{amount} {item}(s) have been added to your shopping list.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the amount.")
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
        messagebox.showinfo("Success", f"{item} has been removed from your shopping list.")
    else:
        messagebox.showerror("Error", f"{item} is not in your shopping list.")

# Function to calculate the total amount of all items
def calculate_total():
    total = sum(shopping_list.values())
    messagebox.showinfo("Total Items", f"Total number of items in the shopping list: {total}")

# Main function
def main():
    global entry_item, entry_amount, listbox

    root = tk.Tk()
    root.title("Shopping List")
    root.geometry("500x600")
    
    style = Style(theme="flatly")
    
    # Create a main frame
    main_frame = ttk.Frame(root, padding="20 20 20 20")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Logo
    label_logo = ttk.Label(main_frame, text="SHOPPING LIST", font=("Helvetica", 24, "bold"), foreground="#3498db")
    label_logo.pack(pady=(0, 20))

    # Input frame
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(fill=tk.X, pady=(0, 20))

    # Item input
    label_item = ttk.Label(input_frame, text="Item:", font=("Helvetica", 12))
    label_item.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="e")
    entry_item = ttk.Entry(input_frame, font=("Helvetica", 12), width=30)
    entry_item.grid(row=0, column=1, pady=5)

    # Amount input
    label_amount = ttk.Label(input_frame, text="Amount:", font=("Helvetica", 12))
    label_amount.grid(row=1, column=0, padx=(0, 10), pady=5, sticky="e")
    entry_amount = ttk.Entry(input_frame, font=("Helvetica", 12), width=30)
    entry_amount.grid(row=1, column=1, pady=5)

    # Buttons frame
    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.pack(fill=tk.X, pady=(0, 20))

    # Add and Remove buttons
    button_add = ttk.Button(buttons_frame, text="Add Item", command=add_item, style="success.TButton")
    button_add.pack(side=tk.LEFT, expand=True, padx=(0, 5))
    button_remove = ttk.Button(buttons_frame, text="Remove Item", command=remove_item, style="danger.TButton")
    button_remove.pack(side=tk.RIGHT, expand=True, padx=(5, 0))

    # Display and Calculate buttons
    button_display = ttk.Button(main_frame, text="Display List", command=display_list, style="info.TButton")
    button_display.pack(fill=tk.X, pady=(0, 10))
    button_calculate = ttk.Button(main_frame, text="Calculate Total", command=calculate_total, style="warning.TButton")
    button_calculate.pack(fill=tk.X)

    # Listbox
    listbox_frame = ttk.Frame(main_frame)
    listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

    listbox = tk.Listbox(listbox_frame, font=("Helvetica", 12), bg="#f0f0f0", selectbackground="#3498db")
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)

    root.mainloop()

# Run the main function
if __name__ == "__main__":
    main()