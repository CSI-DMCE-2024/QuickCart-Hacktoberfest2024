import json
import os


def load_shopping_list():
    if os.path.exists('shopping_list.json'):
        with open('shopping_list.json', 'r') as file:
            return json.load(file)
    return []


def save_shopping_list(shopping_list):
    with open('shopping_list.json', 'w') as file:
        json.dump(shopping_list, file, indent=2)


def toggle_item_check(index):
    shopping_list = load_shopping_list()
    if 0 <= index < len(shopping_list):
        shopping_list[index]['checked'] = not shopping_list[index]['checked']
        save_shopping_list(shopping_list)
        print(f"Toggled: {shopping_list[index]['item']} to {'checked' if shopping_list[index]['checked'] else 'unchecked'}")
    else:
        print("Invalid index.")


def add_item(item_name):
    shopping_list = load_shopping_list()
    if any(item['item'] == item_name for item in shopping_list):
        print(f"Item '{item_name}' already exists in the list.")
        return
    shopping_list.append({"item": item_name, "checked": False})
    save_shopping_list(shopping_list)
    print(f"Added: {item_name}")


def remove_item(index):
    shopping_list = load_shopping_list()
    if 0 <= index < len(shopping_list):
        removed_item = shopping_list.pop(index)
        save_shopping_list(shopping_list)
        print(f"Removed: {removed_item['item']}")
    else:
        print("Invalid index.")


def display_list():
    shopping_list = load_shopping_list()
    print("\nCurrent Shopping List:")
    for index, item in enumerate(shopping_list):
        status = "[x]" if item['checked'] else "[ ]"
        print(f"{index + 1}. {status} {item['item']}")


def main():
    while True:
        display_list()
        print("\nOptions:")
        print("1. Check/Uncheck an item")
        print("2. Add an item")
        print("3. Remove an item by serial number")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ")

        if choice == '1':
            try:
                index = int(input("Enter the serial number of the item to toggle: ")) - 1
                toggle_item_check(index)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '2':
            item_name = input("Enter the name of the item to add: ").strip()
            if item_name:
                add_item(item_name)
            else:
                print("Item name cannot be empty.")
        elif choice == '3':
            try:
                index = int(input("Enter the serial number of the item to remove: ")) - 1
                remove_item(index)
            except ValueError:
                print("Please enter a valid number.")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
