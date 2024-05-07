# from flet import *

# def main(page: Page):
#     page.padding = 50
#     page.window_maximized = True
#     # page.vertical_alignment = MainAxisAlignment.CENTER
#     # page.horizontal_alignment = CrossAxisAlignment.CENTER
#     page.add(
#         ManagerTransactions()
#     )


# app(target=main, assets_dir="../assets")


from Controller.ManagerCRUD import *

getManager(username="admin", password="admin123")
