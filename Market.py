import random


물품명 = [
    "비누", "치약", "샴푸", "린스", "바디워시", "폼클렌징", "칫솔", "수건",
    "휴지", "물티슈", "세탁세제", "섬유유연제", "주방세제", "수세미", "고무장갑",
    "쌀", "라면", "햇반", "생수", "우유", "계란", "두부", "콩나물", "시금치",
    "양파", "감자", "고구마", "사과", "바나나", "오렌지", "귤", "토마토",
    "김치", "된장", "고추장", "간장", "식용유", "참기름", "소금", "설탕",
    "커피", "차", "과자", "빵", "젤리", "초콜릿", "음료수", "맥주", "소주",
    "고기(돼지고기)", "고기(소고기)", "닭고기", "생선", "오징어", "새우", "게",
    "쌀국수", "파스타", "잼", "버터", "치즈", "요거트", "아이스크림", "통조림",
    "냉동만두", "어묵", "햄", "소시지", "김", "미역", "다시마", "멸치",
    "밀가루", "부침가루", "튀김가루", "빵가루", "식초", "소스", "향신료",
    "양초", "성냥", "건전지", "전구", "쓰레기봉투", "지퍼백", "호일", "랩"
]

def GenStorage():
    storage = {}
    for name in 물품명:
        price = random.randint(1, 100) * 100
        num = random.randint(0, 10)
        storage[name] = {"price" : price, "num" : num}

    return storage

def SeeStorage():
    for i, j in storage.items():
        print(i, j, end = " ")
        print()

def buy(storage, WholeMoney):
    
    PriceOfWholeBasket = 0
    while True:
        
        what = input("무엇을 고를까요? ")
        if what not in storage.keys():
            print("없는 상품 입니다 \n")
            continue
        HowMany = int(input("몇 개? "))
        if storage[what]['num'] < HowMany:
            print("갯수 초과입니다. 처음부터 다시 골라주세요 \n")
            continue

        storage[what]['num'] -= HowMany
        PriceOfWholeBasket += storage[what]['price'] * HowMany
        WholeMoney += storage[what]['price'] * HowMany
        


        while True:
            process = input("구매해주셔서 감사합니다 \n 구매 품목 {w} 남은 갯수 {n} \n 계속할까요? 진행 y 취소 n \n".format(w = what, n = storage[what]['num'] ))
            if process == 'y':
                break
            elif process == 'n':
                break
            else: 
                print('제대로 입력하세요!')
        if process == 'y':
            continue
        elif process == 'n':
            print('구매 금액은 {b} 입니다.'.format(b = PriceOfWholeBasket))
            break


    return storage, WholeMoney


# Playing
print("입장")
WholeMoney = 0
while True:
    
    p = input("뭘 하시겠습니까? \n g : 창고 생성, s : 창고 재고 확인, b : 물품 사기, m : 총 비용 확인, q : 그만하기 \n")
    
    if p == 'g':
        storage = GenStorage()
    elif p == 's':
        SeeStorage()
    elif p == 'b':
        storage, WholeMoney = buy(storage, WholeMoney)
    elif p == 'm':
        print("오늘 총 " +  str(WholeMoney) + "원 썼습니다.")
    if p == "q" :
        print('수고하셨습니다.')
        break