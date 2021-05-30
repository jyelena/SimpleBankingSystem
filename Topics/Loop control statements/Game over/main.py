scores = input().split()
mistakes, score = 0, 0
for ch in scores:
    if ch == "I":
        mistakes += 1
        if mistakes == 3:
            break
    elif ch == "C":
        score += 1
print(f"You won\n{score}" if mistakes < 3 else f"Game over\n{score}")
