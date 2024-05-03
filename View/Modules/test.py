# from View.Modules.PersonalEnums import *
#
#
# class ManagerLogin(Container):
#     def __init__(self):
#         super().__init__()
#         self.expand = True
#         self.image_src = "../assets/Login.jpg"
#         self.image_fit = ImageFit.COVER
#         self.alignment = alignment.center
#         self.tf_managerUsername = TextField(
#             label="Username",
#             color=colors.WHITE,
#             text_style=TextStyle(
#                 font_family=str(PoppinsFont.MEDIUM),
#             ),
#             suffix_icon=icons.ACCOUNT_CIRCLE_ROUNDED,
#             border_color=colors.WHITE,
#             border_radius=20,
#         )
#         self.tf_managerPassword = TextField(
#             label="Password",
#             color=colors.WHITE,
#             text_style=TextStyle(
#                 font_family=str(PoppinsFont.MEDIUM),
#             ),
#             password=True,
#             can_reveal_password=True,
#             border_color=colors.WHITE,
#             border_radius=20,
#         )
#         self.content = Column(
#             width=400,
#             horizontal_alignment=CrossAxisAlignment.CENTER,
#             alignment=MainAxisAlignment.CENTER,
#             controls=[
#                 Image(
#                     src=f"../assets/eye.png",
#                 ),
#                 Text(
#                     value="Login",
#                     text_align=TextAlign.CENTER,
#                     size=30,
#                 ),
#                 Container(
#                     margin=margin.only(bottom=15),
#                     content=self.tf_managerUsername,
#                 ),
#                 Container(
#                     margin=margin.only(bottom=15),
#                     content=self.tf_managerPassword,
#                 ),
#                 ElevatedButton(
#                     content=Text(
#                         value="LogIn",
#                         font_family=str(PoppinsFont.BOLD),
#                         size=20,
#                         color=colors.BLACK
#                     ),
#                     style=ButtonStyle(
#                         shape=RoundedRectangleBorder(radius=25)
#                     ),
#                     elevation=10,
#                     bgcolor=colors.WHITE,
#                     width=500,
#                     height=55,
#                 )
#             ]
#         )
#
#     def checkIfEmptyOrBlank(self, textFiled: TextField):
#         if not textFiled.value:
#             textFiled.error_text = "Missing field"
#         else:
#             self.page.go("/main")
#
# def main(page: Page):
#     page.add(
#         ManagerLogin()
#     )
#
#
# app(target=main, assets_dir="../assets")
