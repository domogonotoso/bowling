import random

def MakeClass():
    OneClass = {}
    for i in range(1, random.randint(21, 31)):
        OneClass[i] = MakeScore()
    return OneClass

def MakeScore():
    OneScore = {}
    OneScore['국어']=random.randint(0, 100)
    OneScore['수학']=random.randint(0, 100)
    OneScore['영어']=random.randint(0, 100)
    OneScore['과학']=random.randint(0, 100)
    return OneScore

score = {}
for i in range(1, 7):
    score[f'{i}학년'] = {}
    for j in range(1, random.randint(6, 9)):
        score[f'{i}학년'][f'{j}반'] = MakeClass()

for asd in score.keys():
    print(asd, score[asd])
    print()
    print('-'*20)
    print()


print(score['1학년']['3반'][5])

