import random
import flet as ft

class bowling():

    def __init__ (self, name):
        self.name = name
        self.pin = []
        self.score = []
        self.CumulScore = []

    def random_play(self): 
        for i in range(9):
            first = random.randint(0, 10)
            second = random.randint(0, 10 - first)
            OneFrameScore = [first, second]
            self.pin.append(OneFrameScore)

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
        self.pin.append(TenFrameScore)

        self.ScoreCalculator()
        self.PrintAll()

    def enter_play(self, pin):
        self.pin = pin

        self.ScoreCalculator()
        self.PrintAll()

    def ScoreCalculator(self):
        for i in range(8):
            if self.pin[i][0] == 10 and self.pin[i + 1][0] != 10:
                s = 10 + self.pin[i + 1][0] + self.pin[i + 1][1]
            elif self.pin[i][0] == 10 and self.pin[i + 1][0] == 10 and self.pin[i + 2][0] != 10:
                s = 20 + self.pin[i + 2][0]
            elif self.pin[i][0] == 10 and self.pin[i + 1][0] == 10 and self.pin[i + 2][0] == 10:
                s = 30
            elif self.pin[i][0] + self.pin[i][1] == 10:
                s = 10 + self.pin[i + 1][0]
            else:
                s = self.pin[i][0] + self.pin[i][1]
            self.score.append(s)
        
        if self.pin[8][0] == 10 and self.pin[9][0] != 10:
            nine_s = 10 + self.pin[8][0] + self.pin[9][1]
        elif self.pin[8][0] == 10 and self.pin[9][0] == 10 and self.pin[9][1] != 10:
            nine_s = 20 + self.pin[9][1]
        elif self.pin[8][0] == 10 and self.pin[9][0] == 10 and self.pin[9][1] == 10:
            nine_s = 30
        elif self.pin[8][0] + self.pin[8][1] == 10:
            nine_s = 10 + self.pin[9][0]
        else:
            nine_s = self.pin[8][0] + self.pin[8][1]
        self.score.append(nine_s)

        ten_s = self.pin[9][0] + self.pin[9][1] + self.pin[9][2]
        self.score.append(ten_s)

        self.CumulativeScore()

    def CumulativeScore(self):
        for i in self.score:
            try:
                self.CumulScore.append(i + self.CumulScore[-1])
            except:
                self.CumulScore.append(i)

    def PrintAll(self):
        print(self.name)
        print("*"*30)
        print(self.pin)
        print(self.score)
        print(self.CumulScore)
        print("*"*30)
        print()

    def reset(self):
        self.pin = []
        self.score = []
        self.CumulScore = []

#--------------------------------------
a = bowling('kim')
b = bowling('su')
c = bowling('hwan')

p = [[3, 3], [0, 1], [8, 1], [10, 0], [10, 0], [10, 0], [8, 2], [7, 3], [10, 0], [7, 3, 6]]
d = []
for i in range(9):
    d.append([10, 0])
d.append([10, 10, 10])

a.enter_play(p)
b.enter_play(d)
c.random_play()


#-------------------------------------

def small_box(value, width=35, height=35):
    return ft.Container(
        content=ft.Text(str(value), text_align=ft.TextAlign.CENTER, size=16),
        width=width,
        height=height,
        border=ft.border.all(1, ft.Colors.BLACK),
        padding=0,
    )

def frame_cell(frame, is_tenth=False):
    count = 3 if is_tenth else 2
    boxes = [small_box(v) for v in frame]

    while len(boxes) < count:
        boxes.append(small_box(""))

    return ft.Container(
        content=ft.Row(
            controls=boxes,
            spacing=0,
            tight=True,
        ),
        padding=0,
    )

def score_cell(score, w = 70):
    return ft.Container(
        content=ft.Text(str(score), text_align=ft.TextAlign.CENTER, size=16),
        width=w,
        height=35,
        border=ft.border.all(1, ft.Colors.BLACK),
    )

def main(page: ft.Page):
    page.title = "Bowling"
    page.scroll = ft.ScrollMode.AUTO

    laa = [frame_cell(i) for i in a.pin[:9]] + [frame_cell(a.pin[9], is_tenth=True)]
    lbb = [frame_cell(i) for i in b.pin[:9]] + [frame_cell(b.pin[9], is_tenth=True)]
    lcc = [frame_cell(i) for i in c.pin[:9]] + [frame_cell(c.pin[9], is_tenth=True)]

    la = [score_cell(i) for i in a.CumulScore[:9]] + [score_cell(a.CumulScore[9],  105)] 
    lb = [score_cell(i) for i in b.CumulScore[:9]] + [score_cell(b.CumulScore[9],  105)]
    lc = [score_cell(i) for i in c.CumulScore[:9]] + [score_cell(c.CumulScore[9],  105)]

    page.add(
        ft.Column(
            controls=[
                ft.Text(a.name, size=20, weight=ft.FontWeight.BOLD),
                ft.Row(controls=laa, wrap=True),
                ft.Row(controls=la, wrap=True),

                ft.Text(b.name, size=20, weight=ft.FontWeight.BOLD),
                ft.Row(controls=lbb, wrap=True),
                ft.Row(controls=lb, wrap=True),

                ft.Text(c.name, size=20, weight=ft.FontWeight.BOLD),
                ft.Row(controls=lcc, wrap=True),
                ft.Row(controls=lc, wrap=True),
            ],
            spacing=15,
        )
    )

ft.run(main)