class Info:
    def __init__(self, name, email, num, work):
        self.name = name
        self.email = email
        self.num = num
        self.work = work

def NewSave():
    name = input("Name")
    email = input("Email")
    num = input("Number")
    work = input("work")
    n = Info(name, email, num, work)
    return n

def FindName(Numbook):
    findname = input("Which name do you want to find?")
    for n in Numbook:
        if n.name == findname:
            name = n.name
            email = n.email
            num = n.num
            work = n.work
            break
    print(name, email, num, work)
    return 0



NumBook = []

NumBook.append(NewSave())
NumBook.append(NewSave())
NumBook.append(NewSave())





