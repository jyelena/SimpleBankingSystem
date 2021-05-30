nums = []
while 1:
    num = input()
    if num == ".":
        break
    nums.append(float(num))
print(min(nums))
