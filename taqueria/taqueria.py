# Store the menu of a restaurant in a Dictionary, take orders and calculate the cost

menu = {
    "Baja Taco": 4.00,
    "Burrito": 7.50,
    "Bowl": 8.50,
    "Nachos": 11.00,
    "Quesadilla": 8.50,
    "Super Burrito": 8.50,
    "Super Quesadilla": 9.50,
    "Taco": 3.00,
    "Tortilla Salad": 8.00
    }

# Take the order
sum = 0
try:
    while True:
        item = input(("Item: "))
        # Format the input to match the menu
        item = item.title()
        # Increment the sum if the item is present in the menu, and print it
        if item in menu:
            sum += menu[item]
            print(f"Total: ${sum:.2f}")

# If the user pressed Ctrl + D
except EOFError:
    print()