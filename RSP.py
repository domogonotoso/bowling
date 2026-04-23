import random


RSP = ['R', 'S', 'P']

RSP_rule = {'R' : {'R' : 'draw', 'S' : 'win', 'P' : 'lose'},
            'S' : {'R' : 'lose', 'S' : 'draw', 'P' : 'win'},
            'P' : {'R' : 'win', 'S' : 'lose', 'P' : 'draw'}}

ComRSP = random.randint(0, 3)
ComRSP = RSP[random.randint(0, 3)]

UserWin = 0
ComWin = 0
MatchCount = 0

while True:
    UserRSP = input("Choose R, S, P\n")
    if UserRSP not in ['R', 'S', 'P']:  
        print("Choose correctly!")
        continue

    if RSP_rule[UserRSP][ComRSP] == 'win':
        UserWin += 1
        MatchCount += 1
    elif RSP_rule[UserRSP][ComRSP] == 'lose':
        ComWin += 1
        MatchCount += 1
    elif RSP_rule[UserRSP][ComRSP] == 'draw':
        MatchCount += 1

    print("W-L")
    print("{W}-{L} / {C} matches!".format(W=UserWin, L=ComWin, C=MatchCount))
    
    if UserWin == 3:
        print("You Win!")
        break
    elif ComWin == 3:
        print("You Lose!")
        break
    elif MatchCount == 5:
        print("Draw!")
        break
