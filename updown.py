import random

RandomNum = random.randint(1, 100)


i = 1
while i <= 10:
    num = int(input("숫자 입력하시오: "))
    if num > RandomNum:
        print("Down")
        i += 1
        continue
    elif num < RandomNum:
        print("Up")
        i += 1
    elif num == RandomNum:
        print("Correct!")
        break

