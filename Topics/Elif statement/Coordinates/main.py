x = float(input())
y = float(input())
if x > 0 and y > 0:
    print("I")
elif x < 0 and y > 0:
    print("II")
elif x < 0 and y < 0:
    print("III")
elif x > 0 and y < 0:
    print("IV")
elif (x == 0 and y != 0) or (x != 0 and y == 0):
    print("One of the coordinates is equal to zero!")
else:
    print("It's the origin!")
