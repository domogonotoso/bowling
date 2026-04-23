import random


def play():
    pin = []

    for i in range(9):
        first = random.randint(0, 10)
        second = random.randint(0, 10 - first)
        OneFrameScore = [first, second]
        pin.append(OneFrameScore)

    ten_first = random.randint(0, 10)
    if ten_first == 10:
        ten_second = random.randint(0, 10)
    else:
        ten_second = random.randint(0, 10 - ten_first)
    if ten_second == 10 or (ten_first + ten_second == 10):
        ten_third = random.randint(0, 10)
    elif ten_first + ten_second < 10:
        ten_third = random.randint(0, 10 - ten_first - ten_second)
    elif ten_first == 10 and ten_second < 10:
        ten_third = random.randint(0, 10 - ten_second)

    TenFrameScore = [ten_first, ten_second, ten_third]
    pin.append(TenFrameScore)
    
    return pin

def ScoreCalculator(pin):
    score = []
    for i in range(9):
        if pin[i][0] == 10 and pin[i + 1][0] != 10:
            s = 10 + pin[i + 1][0] + pin[i + 1][1]
        elif pin[i][0] == 10 and pin[i + 1][0] == 10 and pin[i + 2][0] != 10:
            s = 20 + pin[i + 2][0]
        elif pin[i][0] == 10 and pin[i + 1][0] == 10 and pin[i + 2][0] == 10:
            s = 30
        elif pin[i][0] + pin[i][1] == 10:
            s = 10 + pin[i + 1][0]
        else:
            s = pin[i][0] + pin[i][1]
        score.append(s)
    
    if pin[8][0] == 10 and pin[9][0] != 10:
        nine_s = 10 + pin[8][0] + pin[9][1]
    elif pin[8][0] == 10 and pin[9][0] == 10 and pin[9][1] != 10:
        nine_s = 20 + pin[9][1]
    elif pin[8][0] == 10 and pin[9][0] == 10 and pin[9][1] == 10:
        nine_s = 30
    elif pin[8][0] + pin[8][1] == 10:
        nine_s = 10 + pin[9][0]
    else:
        nine_s = pin[8][0] + pin[8][1]
    score.append(nine_s)

    ten_s = pin[9][0] + pin[9][1] + pin[9][2]
    score.append(ten_s)

    return score

def CumulativeScore(score):
    CumulScore = []
    for i in score:
        try:
            CumulScore.append(i + CumulScore[-1])
        except:
            CumulScore.append(i)
    return CumulScore


# pin = [[0, 6], [6, 2], [10, 0], [10, 0], [10, 0], [7, 3], [7, 1], [9, 0], [2, 6], [5, 4, 0]]
pin = play()
score = ScoreCalculator(pin)
CumulScore = CumulativeScore(score)

print(pin)
print(score)
print(CumulScore)