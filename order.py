def BigOrder(list):
    l = len(list)
    while True:
        PreList = []
        for k in list:
            PreList.append(k)

        for i in range(l - 1):
            if list[i] < list[i + 1]:
                change = list[i]
                list[i] = list[i+1]
                list[i + 1] = change
        if PreList == list:
            break
    for j in list:
        print(j)

def SmallOrder(list):
    l = len(list)
    while True:
        PreList = []
        for k in list:
            PreList.append(k)

        for i in range(l - 1):
            if list[i] > list[i + 1]:
                change = list[i]
                list[i] = list[i+1]
                list[i + 1] = change
        if PreList == list:
            break
    for j in list:
        print(j)

list = []
while True:
    num = int(input("Enter Num "))
    list.append(num)
    if len(list) == 3:
        break


c = input("Which one do you want? B? or S?")
if c == 'B':
    BigOrder(list)
elif c == 'S':
    SmallOrder(list)