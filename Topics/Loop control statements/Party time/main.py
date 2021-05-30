guest_list = []
while 1:
    guest_name = input()
    if guest_name == ".":
        break
    guest_list.append(guest_name)
print(guest_list)
print(len(guest_list))
