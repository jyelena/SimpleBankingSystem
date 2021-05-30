price = dict({'chicken': 23, 'goat': 678, 'pig': 1296, 'cow': 3848, 'sheep': 6769})
money = int(input())
(max_price, co) = (0, 0)
an = ''
for animal in price:
    if price[animal] > max_price and money >= price[animal]:
        an = animal
        co = int(money / price[animal])
if co > 0:
    if co != 1 and an != 'sheep':
        an += "s"
    print(co, an)
else:
    print("None")
