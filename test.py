import flet as ft

def main(page: ft.Page):
    txt1 = ft.Text("0")
    txt2 = ft.Text("0", color=ft.Colors.RED)
    txt3 = ft.Text("0")
    txt4 = ft.Text("0")
    txt5 = ft.Text("0")

    count = 0
    frames = list(range(10))
    def roow(n):
        row = ft.Row(
                controls=[
            ft.Container(
                content=ft.Text(str(n +i)),
                width=40,
                height=40,
                border=ft.border.all(1, ft.Colors.BLACK),
            )
            for i in frames
        ]
    )
        return row

    def plus(e):
        nonlocal count
        count +=1
        txt1.value = str(count)
        txt2.value = str(count)
        txt3.value = str(count)
        txt4.value = str(count)
        txt5.value = str(count)
        page.update()

#----------------------------------
    page.add(
        ft.Text("Hello"), txt1,
        ft.Container(
            content=txt2,
            width=100,
            height=50,
            bgcolor=ft.Colors.YELLOW,
            border=ft.border.all(5, ft.Colors.GREEN),
            ),
            ft.Row(spacing = 10,
                   alignment=ft.MainAxisAlignment.CENTER,
    controls=[
        ft.Text("1"),
        txt3,
        ft.Text("2"),
        ft.Text("3"),
    ]
    
),
ft.Row(
    controls=[
        ft.Container(content=ft.Text("A"), expand=1, border=ft.border.all(4, ft.Colors.ORANGE)),
        ft.Container(content=ft.Text("B"), expand=1, border=ft.border.all(4, ft.Colors.PURPLE)),
    ]
),
ft.Column(spacing = 20,
          alignment=ft.MainAxisAlignment.CENTER,
    controls=[
        ft.Text("이름"),
        txt4,
        ft.Text("점수"),
    ]
),
   


        txt5,
        ft.ElevatedButton("증가", on_click=plus),
        ft.Column(
            controls=[
                roow(i) for i in range(1, 51 ,10)
            ]
        )
        

    )

ft.run(main)