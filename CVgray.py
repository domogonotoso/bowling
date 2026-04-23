import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    label="홈",
                    content=ft.Text("홈 화면"),
                ),
                ft.Tab(
                    label="점수",
                    content=ft.Text("점수 화면"),
                ),
                ft.Tab(
                    label="설정",
                    content=ft.Text("설정 화면"),
                ),
            ],
            expand=1,
        )
    )

ft.run(main)