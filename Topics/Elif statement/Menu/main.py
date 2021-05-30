menu = {"pizza":
        ["Margherita", "Four Seasons", "Neapolitan", "Vegetarian", "Spicy"],
        "salad": ["Caesar salad", "Green salad", "Tuna salad", "Fruit salad"],
        "soup": ["Chicken soup", "Ramen", "Tomato soup", "Mushroom cream soup"]}

ask = input()
if ask in menu:
    print(", ".join(menu[ask]))
else:
    print("Sorry, we don't have it in the menu")
