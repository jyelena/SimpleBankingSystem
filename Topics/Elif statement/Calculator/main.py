a = float(input())
b = float(input())
operation = input()
if b == 0.0 and operation in ["/", "div", "mod"]:
    print("Division by 0!")
elif operation == "/":
    print(a / b)
elif operation == "div":
    print(a // b)
elif operation == "mod":
    print(a % b)
elif operation == "pow":
    print(a ** b)
elif operation == "*":
    print(a * b)
elif operation in ["+", "-"]:
    if operation == "-":
        b *= -1
    print(a + b)
