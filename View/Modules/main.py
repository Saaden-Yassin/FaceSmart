from AnimatedControllers import *
from Containers import *


# def navigate(e):
#     match e.control.selected_index:
#         case 0:
#             mainContentContainer.content = DashBoardContent()
#             mainContentContainer.update()
#         case 1:
#             mainContentContainer.content = EmployeesList()
#             mainContentContainer.update()
#         case 2:
#             mainContentContainer.content = ProjectList()
#             mainContentContainer.update()
#         case 5:
#             mainContentContainer.content = Camera()
#             mainContentContainer.update()
#         case 6:
#             leftNavigationBar.page.session.clear()
#             leftNavigationBar.page.go("/")
#             leftNavigationBar.page.update()
#         case _:
#             mainContentContainer.content = Container(
#                 alignment=alignment.center,
#                 expand=True,
#                 content=Text(
#                     value="TO DO",
#                     font_family=str(PoppinsFont.BOLD),
#                     size=50
#                 )
#             )
#             mainContentContainer.update()


# mainContentContainer = Container(
#     col=9.7,
#     margin=0,
#     expand=True,
#     content=DashBoardContent()
# )
#
# leftNavigationBar = LeftNavigationBar()
# leftNavigationBar.on_change = navigate


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
                    ManagerTransactions(page)
                ],
                padding=0
            )
        )
        if page.route == "/home":
            username = page.session.get("username")
            if username:
                def navigate(e):
                    match e.control.selected_index:
                        case 0:
                            mainContentContainer.content = DashBoardContent(username=username)
                            mainContentContainer.update()
                        case 1:
                            mainContentContainer.content = EmployeesList()
                            mainContentContainer.update()
                        case 2:
                            mainContentContainer.content = ProjectList()
                            mainContentContainer.update()
                        case 5:
                            mainContentContainer.content = Camera()
                            mainContentContainer.update()
                        case 6:
                            leftNavigationBar.page.session.clear()
                            page.go("/")
                            page.update()
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
                    content=DashBoardContent(username=username)
                )

                leftNavigationBar = LeftNavigationBar()
                leftNavigationBar.on_change = navigate

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
            else:
                page.go("/")
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


app(target=main, assets_dir="../assets")
