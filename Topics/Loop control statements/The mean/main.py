nums = []
s = 0
while 1:
    num = input()
    if num == ".":
        break
    nums.append(int(num))
    s += int(num)
print(s / len(nums))
