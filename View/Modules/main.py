from Containers import *

from Model.ConnectionToDB import *

def navigate(e):
    match e.control.selected_index:
        case 0:
            mainContentContainer.content = DashBoardContent(
                username="SAADEN Yassin"
            )
            mainContentContainer.update()
        case 1:
            mainContentContainer.content = EmployeesList()
            mainContentContainer.update()
        case 5:
            mainContentContainer.content = Camera()
            mainContentContainer.update()
        case _:
            mainContentContainer.content = Container(
                alignment=alignment.center,
                expand=True,
                content=Text(
                    value="TO DO",
                    font_family=str(PoppinsFont.BOLD),
                    size=50
                )
            )
            mainContentContainer.update()


mainContentContainer = Container(
    col=9.7,
    margin=0,
    expand=True,
    content=EmployeesList()
)

leftNavigationBar = LeftNavigationBar()
leftNavigationBar.on_change = navigate


def main(page: Page):
    page.window_maximized = True
    page.theme_mode = ThemeMode.DARK
    page.window_min_width = 1350
    page.platform = PagePlatform.WINDOWS
    fontDicts = {}
    for font in PoppinsFont:
        fontDicts[str(font)] = font.value

    page.fonts = fontDicts

    def route_change(route):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    Container(
                        image_src=f"../assets/bgLeftNavBar.jpg",
                        image_fit=ImageFit.COVER,
                        alignment=alignment.center,
                        expand=True,
                        content=ManagerLogin(
                            bgColor=colors.with_opacity(color=colors.BLACK, opacity=0.5)
                        )
                    ),
                ],
                padding=0
            )
        )
        if page.route == "/home":
            page.padding = 0
            page.views.append(
                View(
                    "/home",
                    [
                        Container(
                            margin=0,
                            padding=0,
                            image_src=f"../assets/bgLeftNavBar.jpg",
                            image_fit=ImageFit.COVER,
                            expand=True,
                            content=ResponsiveRow(
                                spacing=0,
                                expand=True,
                                controls=[
                                    Container(
                                        col=2.3,
                                        bgcolor=colors.with_opacity(color=colors.BLACK, opacity=0.7),
                                        content=leftNavigationBar,
                                    ),
                                    mainContentContainer
                                ]
                            )
                        )
                    ],
                    padding=0,
                )
            )
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


app(target=main, assets_dir="../assets")
