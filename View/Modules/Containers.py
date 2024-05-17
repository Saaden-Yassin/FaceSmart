from PersonalControllers import *
from PersonalEnums import AppColors
from Controller.ManagerCRUD import *
from Controller.ScheduleCRUD import *
import base64
from threading import Thread
import cv2
import face_recognition
import numpy as np


# region DashBoardContent
class DashBoardContent(Column):

    def __init__(self, col: int | float = None, username: str = "John Doe"):
        super().__init__()
        self.expand = True
        EmployeesCard.totalEmployees = getTotalNumberOfEmployees()
        self.scroll = ScrollMode.ALWAYS
        self.col = col,
        self.spacing = 0
        self.controls = [
            Container(
                padding=padding.only(top=65, right=30, bottom=50, left=20),
                content=Column(
                    controls=[
                        ResponsiveRow(
                            controls=[
                                Container(
                                    DashBoardImage(username)
                                )
                            ]
                        ),
                        Column(
                            spacing=30,
                            controls=[
                                Container(
                                    content=ResponsiveRow(
                                        controls=[
                                            Container(
                                                col=9,
                                                height=450,
                                                border_radius=25,
                                                bgcolor=colors.BLACK,
                                                padding=25,
                                                content=Column(
                                                    controls=[
                                                        Row(
                                                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                                                            controls=[
                                                                Text(
                                                                    value="Project statistics",
                                                                    color=colors.BLUE,
                                                                    font_family=str(PoppinsFont.MEDIUM),
                                                                    size=16.1
                                                                ),
                                                                ElevatedButton(
                                                                    bgcolor=colors.TRANSPARENT,
                                                                    color="#1D7D81",
                                                                    content=Text(
                                                                        value="View All",
                                                                        size=16.1,
                                                                        weight=FontWeight.BOLD
                                                                    ),
                                                                    on_click=self.viewProjects
                                                                )
                                                            ]
                                                        ), Container(
                                                            margin=margin.only(top=25),
                                                            content=Column(
                                                                controls=[
                                                                    ProjectInfoContainer(
                                                                        progressValue=ProjectState[
                                                                            getSortedProjectByDayLeft()[
                                                                                0].status].value,
                                                                        progressBgColor="#172336",
                                                                        progressColor="#465F85",
                                                                        projectName=getSortedProjectByDayLeft()[0].name,
                                                                        projectDaysLeft=getTimeLeftForDeadline(
                                                                            getSortedProjectByDayLeft()[0])
                                                                    ),
                                                                    ProjectInfoContainer(
                                                                        progressValue=ProjectState[
                                                                            getSortedProjectByDayLeft()[
                                                                                1].status].value,
                                                                        progressBgColor="#2B1D2C",
                                                                        progressColor="#844685",
                                                                        projectName=getSortedProjectByDayLeft()[1].name,
                                                                        projectDaysLeft=getTimeLeftForDeadline(
                                                                            getSortedProjectByDayLeft()[1])
                                                                    ),
                                                                    ProjectInfoContainer(
                                                                        progressValue=ProjectState[
                                                                            getSortedProjectByDayLeft()[
                                                                                2].status].value,
                                                                        progressBgColor="#3F3023",
                                                                        progressColor="#C55D42",
                                                                        projectName=getSortedProjectByDayLeft()[2].name,
                                                                        projectDaysLeft=getTimeLeftForDeadline(
                                                                            getSortedProjectByDayLeft()[2])
                                                                    )
                                                                ]
                                                            )
                                                        )

                                                    ]  # END column content
                                                )
                                            ),
                                            Calendar(
                                                col=3,
                                                bgcolor=colors.BLACK,
                                                # opacity=0.65,
                                                border_radius_=25,
                                                height=450,
                                                padding_=padding.only(top=60),
                                            )
                                        ]
                                    )
                                ),
                                ResponsiveRow(
                                    # spacing=50,
                                    controls=[
                                        ResponsiveRow(
                                            col=9,
                                            controls=[
                                                Container(
                                                    expand=True,
                                                    alignment=alignment.center,
                                                    content=ResponsiveRow(
                                                        controls=[
                                                            EmployeesCard(
                                                                col=4,
                                                                title="TOTAL EMPLOYEES",
                                                                titleColor="#65B0FF",
                                                                shadowColor="#65B0FF",
                                                                iconColor="#0012FF",
                                                                nbrEmployees=getTotalNumberOfEmployees(),
                                                                totalEmployees=getTotalNumberOfEmployees(),
                                                                progressIndicatorBgColor="#160364",
                                                                progressIndicatorColor="#5584FF",
                                                                progressBarColor="#3300FE",
                                                                progressBarBgColor="#192C50"
                                                            ),
                                                            EmployeesCard(
                                                                col=4,
                                                                title="ACTIVE EMPLOYEES",
                                                                titleColor="#93FFAE",
                                                                shadowColor="#93FFAE",
                                                                iconName=icons.GROUP_ADD_ROUNDED,
                                                                iconColor="#00FE40",
                                                                nbrEmployees=getNumberEmployeesActive(),
                                                                totalEmployees=getTotalNumberOfEmployees(),
                                                                progressIndicatorBgColor="#0A2F0B",
                                                                progressIndicatorColor="#6DFF55",
                                                                progressBarColor="#00FE40",
                                                                progressBarBgColor="#192C50"
                                                            ),
                                                            EmployeesCard(
                                                                col=4,
                                                                title="INACTIVE EMPLOYEES",
                                                                titleColor="#FF7373",
                                                                shadowColor="#FF7373",
                                                                iconName=icons.GROUP_REMOVE_ROUNDED,
                                                                iconColor="#FF0000",
                                                                nbrEmployees=getNumberEmployeesInactive(),
                                                                totalEmployees=getTotalNumberOfEmployees(),
                                                                progressIndicatorBgColor="#441717",
                                                                progressIndicatorColor="#FF0000",
                                                                progressBarColor="#FF0000",
                                                                progressBarBgColor="#192C50"
                                                            )
                                                        ]
                                                    )
                                                )
                                            ]
                                        ),
                                        EmployeesInOutContainer(
                                            col=3,
                                            employeeID=getLastCheckinOrLastCheckout()[0],
                                            circleImageBase64Src=getLastCheckinOrLastCheckout()[1],
                                            employeeName=getLastCheckinOrLastCheckout()[2],
                                            hour=getLastCheckinOrLastCheckout()[3],
                                            check=getLastCheckinOrLastCheckout()[4]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ),
        ]

    def viewProjects(self, e):
        pass


# endregion

# region EmployeesList
class EmployeesList(Container):
    def __init__(self):
        super().__init__()
        self.padding = 16
        self.dataRows = []
        self.isAscendant: bool = False
        self.animatedSearchBar = AnimatedSearchBar()
        self.animatedSearchBar.onChange(self.searchEmployee)
        self.dataTable = DataTable(
            gradient=AppColors.BLACK_GREEN_LINEAR_GRADIAN.value,
            data_row_max_height=80,
            horizontal_lines=BorderSide(
                width=3,
                color="#988787"
            ),
            sort_column_index=2,
            sort_ascending=False,
            column_spacing=12,
            columns=[
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Image",
                        color="#1D7D81",
                    ),
                ),
                DataColumn(
                    numeric=True,
                    label=TableHeadingContainer(
                        textValue="ID",
                        color="#1D7D81",
                        enableSort=True,
                        onSortClick=lambda _: self.sortEmployeesList(sortCriteria="ID")
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="First name",
                        color="#1D7D81",
                        enableSort=True,
                        onSortClick=lambda _: self.sortEmployeesList(sortCriteria="firstName")
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Last name",
                        color="#1D7D81",
                        enableSort=True,
                        onSortClick=lambda _: self.sortEmployeesList(sortCriteria="lastName")
                    ),
                ),
                DataColumn(
                    numeric=True,
                    label=TableHeadingContainer(
                        textValue="Age",
                        color="#1D7D81",
                        enableSort=True,
                        onSortClick=lambda _: self.sortEmployeesList(sortCriteria="age")
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Email",
                        color="#1D7D81",
                        enableSort=True,
                        onSortClick=lambda _: self.sortEmployeesList(sortCriteria="email")
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Department",
                        color="#1D7D81",
                        enableSort=True,
                        onSortClick=lambda _: self.sortEmployeesList(sortCriteria="departmentId"),
                        enableFilter=True,
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Current project",
                        color="#1D7D81",
                        enableSort=True,
                        onSortClick=lambda _: self.sortEmployeesList(sortCriteria="projectId"),
                        enableFilter=True
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Status",
                        color="#1D7D81",
                        enableFilter=True
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Delete",
                        color="#1D7D81",
                    ),
                )
            ],
            rows=self.dataRows
        )
        self.content = Column(
            spacing=50,
            controls=
            [
                Container(
                    margin=margin.only(top=70, left=16),
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            self.animatedSearchBar,
                            ElevatedButton(
                                content=Text(
                                    value="Add Employee",
                                    size=16.1,
                                    color=colors.WHITE
                                ),
                                height=50,
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(
                                        radius=5
                                    ),
                                    bgcolor="#1D7D81",
                                    overlay_color="#9cbab7"
                                ),
                                on_click=self.showEmployeeDialog
                            )
                        ]
                    )
                ),
                Column(
                    scroll=ScrollMode.ALWAYS,
                    expand=True,
                    controls=[
                        Row(
                            scroll=ScrollMode.ADAPTIVE,
                            controls=[
                                self.dataTable
                            ]
                        )
                    ]
                )
            ]
        )

    def sortEmployeesList(self, sortCriteria: str = id):
        self.isAscendant = not self.isAscendant
        flag = self.isAscendant
        sortdEmployees = getEmployeesTableSorted(
            criteria=sortCriteria,
            sortMode="ASC" if flag else "DESC"
        )
        self.dataRows.clear()
        self.dataRows.extend(
            map(
                lambda emp: (
                    EmployeeDataRow(
                        id=emp.ID,
                        imageSrcBase64=emp.image,
                        firstName=emp.firstName,
                        lastName=emp.lastName,
                        age=emp.age,
                        email=emp.email,
                        department=emp.departmentName,
                        currentProject=emp.projectName,
                        status=emp.status,
                        dataTable=self.dataTable
                    )
                ),
                sortdEmployees
            )
        )
        self.update()

    def did_mount(self):
        Thread(target=self.loadData, daemon=True).start()

    def loadData(self):
        if getEmployees():
            self.dataRows.extend(
                map(
                    lambda emp: (
                        EmployeeDataRow(
                            id=emp.ID,
                            imageSrcBase64=emp.image,
                            firstName=emp.firstName,
                            lastName=emp.lastName,
                            age=emp.age,
                            email=emp.email,
                            department=emp.departmentName,
                            currentProject=emp.projectName,
                            status=emp.status,
                            dataTable=self.dataTable
                        )
                    ),
                    getEmployees()
                )
            )
        self.update()

    def showEmployeeDialog(self, e):
        addEmployeeDialog = AddEmployeeDialog(self)
        self.page.dialog = addEmployeeDialog
        addEmployeeDialog.open = True
        addEmployeeDialog.dialogEBAddEmployee.on_click = lambda _: self.addEmployee(
            image=addEmployeeDialog.localImagePicker.getPickedEncodedImage(),
            firstName=addEmployeeDialog.dialogTFFirstName.value,
            lastName=addEmployeeDialog.dialogTFLastName.value,
            age=addEmployeeDialog.dialogTFAge.value,
            email=addEmployeeDialog.dialogTFEmail.value,
            department=addEmployeeDialog.dialogDDDepartment.value,
            currentProject=addEmployeeDialog.dialogTFCurrentProject.value,
        )
        self.page.update()

    def addEmployee(self, image: str, firstName: str, lastName: str, age: str,
                    email: str, department: str,
                    currentProject: str = "Current project"):
        if image != "" and firstName != "" and lastName != "" and age != 0 and email != "" and department != "":
            if createEmployee(Employee(image=image, firstName=firstName, lastName=lastName, age=age, email=email,
                                       departmentName=department, projectName=currentProject)):
                self.dataRows.append(
                    EmployeeDataRow(
                        id=getEmployees()[-1].ID,
                        imageSrcBase64=getEmployees()[-1].image,
                        firstName=getEmployees()[-1].firstName,
                        lastName=getEmployees()[-1].lastName,
                        age=getEmployees()[-1].age,
                        email=getEmployees()[-1].email,
                        department=getEmployees()[-1].departmentName,
                        currentProject=getEmployees()[-1].projectName,
                        status=getEmployees()[-1].status,
                        dataTable=self.dataTable
                    )
                )
            self.update()

    def searchEmployee(self, e):
        value = self.animatedSearchBar.getSearchEntry().lower()
        if value != "":
            filteredEmp = filter(
                lambda emp: (
                    str(emp.ID).find(value) != -1
                    or emp.firstName.lower().find(value) != -1
                    or emp.lastName.lower().find(value) != -1
                    or str(emp.age).find(value) != -1
                    or emp.email.lower().find(value) != -1
                    or emp.projectName.lower().find(value) != -1 if emp.projectName else None
                ), getEmployees()
            )
            self.dataRows.clear()
            self.dataRows.extend(
                map(
                    lambda emp: EmployeeDataRow(
                        id=emp.ID,
                        imageSrcBase64=emp.image,
                        firstName=emp.firstName,
                        lastName=emp.lastName,
                        age=emp.age,
                        email=emp.email,
                        department=emp.departmentName,
                        currentProject=emp.projectName,
                        status=emp.status,
                        dataTable=self.dataTable
                    ), filteredEmp
                )
            )
        else:
            self.dataRows.clear()
            self.loadData()
        self.update()


# endregion

# region ManagerRegister
class ManagerRegister(Container):
    def __init__(self, rootPage: Page, bgColor: str = None):
        super().__init__()
        self.bgcolor = bgColor
        self.rootPage = rootPage
        self.padding = padding.only(left=20, right=20, top=16, bottom=16)
        self.border_radius = 40
        self.height = 800
        self.animate_opacity = animation.Animation(duration=2000, curve=AnimationCurve.EASE)
        self.pickedEncodedImage: str = ""
        self.tf_managerFirstName = TextField(
            label="First name",
            color=colors.WHITE,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM),
            ),
            prefix_icon=icons.ACCOUNT_CIRCLE_OUTLINED,
            border_color=colors.WHITE,
            border_radius=20,
        )
        self.tf_managerLastName = TextField(
            label="Last name",
            color=colors.WHITE,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM),
            ),
            prefix_icon=icons.ACCOUNT_CIRCLE_OUTLINED,
            border_color=colors.WHITE,
            border_radius=20,
        )
        self.tf_managerUsername = TextField(
            label="Username",
            color=colors.WHITE,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM),
            ),
            prefix_icon=icons.ACCOUNT_CIRCLE_ROUNDED,
            border_color=colors.WHITE,
            border_radius=20,
        )
        self.tf_managerPassword = TextField(
            label="Password",
            color=colors.WHITE,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM),
            ),
            password=True,
            prefix_icon=icons.LOCK_ROUNDED,
            can_reveal_password=True,
            border_color=colors.WHITE,
            border_radius=20,
        )
        self.tf_managerConfirmPassword = TextField(
            label="Confirm password",
            color=colors.WHITE,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM),
            ),
            prefix_icon=icons.LOCK_OUTLINE_ROUNDED,
            border_color=colors.WHITE,
            border_radius=20,
        )
        self.tf_managerAge = TextField(
            label="Age",
            color=colors.WHITE,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM),
            ),
            prefix_icon=icons.ACCOUNT_CIRCLE_OUTLINED,
            border_color=colors.WHITE,
            border_radius=20,
        )
        self.tf_managerEmail = TextField(
            label="Email",
            color=colors.WHITE,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM),
            ),
            prefix_icon=icons.MAIL_ROUNDED,
            border_color=colors.WHITE,
            border_radius=20,
        )
        self.eb_register = ElevatedButton(
            content=Text(
                value="Register",
                font_family=str(PoppinsFont.BOLD),
                size=20,
                color=colors.BLACK,
            ),
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=25)
            ),
            elevation=10,
            bgcolor=colors.WHITE,
            width=200,
            height=55,
        )
        self.eb_login = ElevatedButton(
            bgcolor=colors.TRANSPARENT,
            elevation=0,
            content=Text(
                value="Back to login",
                font_family=str(PoppinsFont.BOLD),
                size=15,
                color="#1D7D81",
            ),
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=25),

            ),
            width=200,
            height=55,
        )
        self.localImagePicker = LocalImagePicker(
            rootPage=self.rootPage,
            margin_=margin.only(bottom=25),
            btnPickImage=FilledButton(
                content=Row(
                    controls=[
                        Icon(
                            name=icons.UPLOAD_FILE_ROUNDED,
                            color=colors.WHITE
                        ),
                        Text(
                            value="Click to upload image(optional)",
                            font_family=str(PoppinsFont.BOLD),
                            color=colors.WHITE
                        )
                    ]
                ),
                height=55,
                style=ButtonStyle(
                    bgcolor=colors.TRANSPARENT,
                    shape=RoundedRectangleBorder(radius=15),
                    side=BorderSide(width=1, color=colors.WHITE),
                )
            ),
            showPickedImageName=Text(
                font_family=str(PoppinsFont.BOLD_ITALIC),
                size=13,
                color=colors.BLUE,
            ),
        )
        self.content = Column(
            spacing=5,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            scroll=ScrollMode.ALWAYS,
            width=400,
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Container(
                    margin=margin.only(top=15),
                    content=Image(
                        src=f"../assets/eye.png",
                        filter_quality=FilterQuality.HIGH,
                    ),
                ),
                Container(
                    margin=margin.only(bottom=50),
                    content=Text(
                        value="Register",
                        text_align=TextAlign.CENTER,
                        size=30,
                    )
                ),
                Container(
                    margin=margin.only(bottom=15),
                    content=self.tf_managerFirstName,
                ),
                Container(
                    margin=margin.only(bottom=15),
                    content=self.tf_managerLastName,
                ),
                Container(
                    margin=margin.only(bottom=15),
                    content=self.tf_managerUsername,
                ),
                Container(
                    margin=margin.only(bottom=15),
                    content=self.tf_managerAge,
                ),
                Container(
                    margin=margin.only(bottom=15),
                    content=self.tf_managerEmail,
                ),
                Container(
                    margin=margin.only(bottom=15),
                    content=self.tf_managerPassword,
                ),
                self.localImagePicker,
                self.eb_register,
                self.eb_login
            ]
        )

    def closeBanner(self, e):
        self.rootPage.banner.open = False
        self.rootPage.update()

    def validateRegister(self) -> bool:
        firstName = self.tf_managerFirstName.value
        lastName = self.tf_managerLastName.value
        username = self.tf_managerUsername.value
        password = self.tf_managerPassword.value
        age = self.tf_managerAge.value
        email = self.tf_managerEmail.value
        image = self.pickedEncodedImage
        print("ManagerImg -> ", image)
        if not ValidateReg.validate(firstName, ValidateReg.FIRST_LAST_NAME.value[0]):
            self.tf_managerFirstName.error_text = ValidateReg.FIRST_LAST_NAME.value[
                1] if firstName else "Missing first name!!!"
            self.tf_managerFirstName.update()
            flag = False
        else:
            self.tf_managerFirstName.error_text = ""
            self.tf_managerFirstName.update()
            flag = True

        if not ValidateReg.validate(lastName, ValidateReg.FIRST_LAST_NAME.value[0]):
            self.tf_managerLastName.error_text = ValidateReg.FIRST_LAST_NAME.value[
                1] if lastName else "Missing last name!!!"
            self.tf_managerLastName.update()
            flag = False
        else:
            self.tf_managerLastName.error_text = ""
            self.tf_managerLastName.update()
            flag = True

        if not ValidateReg.validate(username, ValidateReg.USERNAME.value[0]):
            self.tf_managerUsername.error_text = ValidateReg.USERNAME.value[
                1] if username else "Missing username!!!"
            self.tf_managerUsername.update()
            flag = False
        else:
            self.tf_managerUsername.error_text = ""
            self.tf_managerUsername.update()
            flag = True

        if not ValidateReg.validate(email, ValidateReg.EMAIL.value[0]):
            self.tf_managerEmail.error_text = ValidateReg.EMAIL.value[1] if email else "Missing email!!!"
            self.tf_managerEmail.update()
            flag = False
        else:
            self.tf_managerEmail.error_text = ""
            self.tf_managerEmail.update()
            flag = True

        if not ValidateReg.validate(age, ValidateReg.AGE.value[0]):
            self.tf_managerAge.error_text = ValidateReg.AGE.value[1] if age else "Missing age!!!"
            self.tf_managerAge.update()
            flag = False
        else:
            self.tf_managerAge.error_text = ""
            self.tf_managerAge.update()
            flag = True

        if not ValidateReg.validate(password, ValidateReg.PASSWORD.value[0]):
            self.tf_managerPassword.error_text = ValidateReg.PASSWORD.value[1] if password else "Missing password!!!"
            self.tf_managerPassword.update()
            flag = False
        else:
            self.tf_managerPassword.error_text = ""
            self.tf_managerPassword.update()
            flag = True

        if flag:
            if not getManager(username=username, password=password, image=image):
                if createManager(
                        Manager(
                            firstName=firstName,
                            lastName=lastName,
                            age=int(age),
                            email=email,
                            username=username,
                            password=password,
                            image=self.localImagePicker.getPickedEncodedImage()
                        )
                ):
                    flag = True
                else:
                    flag = False
            else:
                self.rootPage.banner = Banner(
                    bgcolor=colors.PINK_200,
                    leading=Icon(
                        icons.WARNING_AMBER_ROUNDED,
                        color=colors.PINK_600,
                        size=45
                    ),
                    content=Text(
                        value="Oops, manager already exists",
                        font_family=str(PoppinsFont.BOLD),
                        color=colors.PINK_600
                    ),
                    actions=[
                        TextButton(
                            on_click=self.closeBanner,
                            content=Text(
                                value="Close",
                                font_family=str(PoppinsFont.BOLD),
                                color=colors.PINK_800
                            )
                        ),
                    ],
                )
                self.rootPage.banner.open = True
                self.rootPage.update()
                flag = False
        return flag

    # endregion


# endregion

# region ManagerLogin
class ManagerLogin(Container):
    def __init__(self, bgColor: str = None, rootPage: Page = None):
        super().__init__()
        self.bgcolor = bgColor
        self.padding = padding.only(left=20, right=20)
        self.border_radius = 40
        self.opacity = 1
        self.animate_opacity = animation.Animation(duration=2000, curve=AnimationCurve.EASE)
        self.tf_managerUsername = TextField(
            label="Username",
            color=colors.WHITE,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM),
            ),
            suffix_icon=icons.ACCOUNT_CIRCLE_ROUNDED,
            border_color=colors.WHITE,
            border_radius=20,
        )
        self.tf_managerPassword = TextField(
            label="Password",
            color=colors.WHITE,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM),
            ),
            password=True,
            can_reveal_password=True,
            border_color=colors.WHITE,
            border_radius=20,
        )
        self.eb_login = ElevatedButton(
            content=Text(
                value="LogIn",
                font_family=str(PoppinsFont.BOLD),
                size=20,
                color=colors.BLACK,
            ),
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=25)
            ),
            elevation=10,
            bgcolor=colors.WHITE,
            width=200,
            height=55,
            on_click=self.validateLogin,
        )
        self.eb_register = ElevatedButton(
            bgcolor=colors.TRANSPARENT,
            elevation=0,
            content=Text(
                value="Or register",
                font_family=str(PoppinsFont.BOLD),
                size=15,
                color="#1D7D81",
            ),
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=25),

            ),
            width=200,
            height=55,
        )
        self.rootPage = rootPage
        self.content = Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.CENTER,
            width=500,
            height=600,
            spacing=15,
            controls=[
                Container(
                    margin=margin.only(top=15),
                    content=Image(
                        src=f"../assets/eye.png",
                        filter_quality=FilterQuality.HIGH,
                    ),
                ),
                Container(
                    margin=margin.only(bottom=50),
                    content=Text(
                        value="Login",
                        text_align=TextAlign.CENTER,
                        size=30,
                    ),
                ),
                Container(
                    margin=margin.only(bottom=15),
                    content=self.tf_managerUsername,
                ),
                Container(
                    margin=margin.only(bottom=15),
                    content=self.tf_managerPassword,
                ),
                Row(
                    alignment=MainAxisAlignment.SPACE_EVENLY,
                    controls=[
                        self.eb_login,
                        self.eb_register
                    ]
                ),
                # ElevatedButton(
                #     text="Go to home page ->",
                #     on_click=lambda _: self.rootPage.go("/home"),
                # )
            ]
        )

    def closeBanner(self, e):
        self.rootPage.banner.open = False
        self.rootPage.update()

    def validateLogin(self, e):
        username = self.tf_managerUsername.value
        password = self.tf_managerPassword.value

        if not ValidateReg.validate(username, ValidateReg.USERNAME.value[0]):
            self.tf_managerUsername.error_text = ValidateReg.USERNAME.value[
                1] if username else "Missing username"
            self.tf_managerUsername.update()
            flag = False
        else:
            self.tf_managerUsername.error_text = ""
            self.tf_managerUsername.update()
            flag = True
        if not ValidateReg.validate(password, ValidateReg.PASSWORD.value[0]):
            self.tf_managerPassword.error_text = ValidateReg.PASSWORD.value[1] if password else "Missing password"
            self.tf_managerPassword.update()
            flag = False
        else:
            self.tf_managerPassword.error_text = ""
            self.tf_managerPassword.update()
            flag = True
        if flag:
            if getManager(username=username, password=password):
                self.page.session.set(key="username", value=username)
                DashBoardContent.username = username
                self.page.go("/home")
                self.page.update()
            else:
                self.rootPage.banner = Banner(
                    bgcolor=colors.PINK_200,
                    leading=Icon(
                        icons.WARNING_AMBER_ROUNDED,
                        color=colors.PINK_600,
                        size=45
                    ),
                    content=Text(
                        value="Oops, there is no manager with the given username and password",
                        font_family=str(PoppinsFont.BOLD),
                        color=colors.PINK_600
                    ),
                    actions=[
                        TextButton(
                            on_click=self.closeBanner,
                            content=Text(
                                value="Close",
                                font_family=str(PoppinsFont.BOLD),
                                color=colors.PINK_800
                            )
                        ),
                    ],
                )
                self.rootPage.banner.open = True
                self.rootPage.update()


# endregion

# region ManagerTransactions
class ManagerTransactions(Container):
    def __init__(self, rootPage: Page):
        super().__init__()
        self.alignment = alignment.center
        self.image_src = f"../assets/BgImage.jpg"
        self.image_fit = ImageFit.COVER
        self.rootPage = rootPage
        self.expand = True
        self.managerLogin = ManagerLogin(
            bgColor=colors.with_opacity(opacity=0.7, color=colors.BLACK),
            rootPage=self.rootPage
        )
        self.managerLogin.eb_register.on_click = self.switchToRegister
        self.managerRegister = ManagerRegister(
            rootPage=self.rootPage,
            bgColor=colors.with_opacity(opacity=0.7, color=colors.BLACK)
        )
        self.managerRegister.eb_register.on_click = self.switchToLoginWithVerification
        self.managerRegister.eb_login.on_click = self.switchToLogin
        self.managerRegister.visible = False
        self.managerRegister.opacity = 0
        self.stack = Stack(
            controls=[
                self.managerRegister,
                self.managerLogin
            ]
        )
        self.content = self.stack

    def switchToRegister(self, e):
        self.managerLogin.opacity = 0
        self.managerLogin.update()
        sleep(0.9)
        self.managerLogin.visible = False
        self.managerLogin.update()
        self.managerRegister.visible = True
        self.managerRegister.update()
        sleep(0.9)
        self.managerRegister.opacity = 1
        self.managerRegister.update()

    def switchToLoginWithVerification(self, e):
        if self.managerRegister.validateRegister():
            self.switchToLogin(e)

    def switchToLogin(self, e):
        self.managerRegister.opacity = 0
        self.managerRegister.update()
        sleep(0.9)
        self.managerRegister.visible = False
        self.managerRegister.update()
        self.managerLogin.visible = True
        self.managerLogin.update()
        sleep(0.9)
        self.managerLogin.opacity = 1
        self.managerLogin.update()

    # endregion


# endregion

# region ProjectList
class ProjectList(Container):
    def __init__(self):
        super().__init__()
        self.padding = padding.only(top=70, left=16, right=16)
        self.animatedSearchBar = AnimatedSearchBar()
        self.animatedSearchBar.onChange(self.searchProject)
        self.dataRows = []
        self.isAscendant: bool = False
        self.dataTable = DataTable(
            columns=[
                DataColumn(
                    TableHeadingContainer(
                        textValue="ID",
                        enableSort=True,
                        onSortClick=lambda _: self.sortProjectsList(sortCriteria="ID"),
                        color="#1D7D81",
                    )
                ),
                DataColumn(
                    TableHeadingContainer(
                        textValue="Project name",
                        enableSort=True,
                        onSortClick=lambda _: self.sortProjectsList(sortCriteria="name"),
                        color="#1D7D81",
                    )
                ),
                DataColumn(
                    TableHeadingContainer(
                        textValue="Start date",
                        enableSort=True,
                        onSortClick=lambda _: self.sortProjectsList(sortCriteria="startDate"),
                        color="#1D7D81",
                    )
                ),
                DataColumn(
                    TableHeadingContainer(
                        textValue="End date",
                        enableSort=True,
                        onSortClick=lambda _: self.sortProjectsList(sortCriteria="endDate"),
                        color="#1D7D81",
                    )
                ),
                DataColumn(
                    TableHeadingContainer(
                        textValue="Status",
                        enableFilter=True,
                        color="#1D7D81",
                    )
                ),
                DataColumn(
                    TableHeadingContainer(
                        textValue="Delete",
                        color="#1D7D81",
                    )
                )
            ],
            rows=self.dataRows
        )
        self.content = Column(
            controls=[
                Container(
                    margin=margin.only(bottom=50),
                    content=Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            self.animatedSearchBar,
                            ElevatedButton(
                                content=Text(
                                    value="Add Project",
                                    size=16.1,
                                    color=colors.WHITE
                                ),
                                height=50,
                                style=ButtonStyle(
                                    shape=RoundedRectangleBorder(
                                        radius=5
                                    ),
                                    bgcolor="#1D7D81",
                                    overlay_color="#9cbab7"
                                ),
                                on_click=self.showProjectDialog
                            )
                        ]
                    )
                ),
                Container(
                    gradient=AppColors.BLACK_GREEN_LINEAR_GRADIAN.value,
                    content=Column(
                        scroll=ScrollMode.ALWAYS,
                        expand=True,
                        controls=[
                            Row(
                                scroll=ScrollMode.ADAPTIVE,
                                controls=[
                                    self.dataTable
                                ]
                            )
                        ]
                    )
                )
            ]
        )

    def did_mount(self):
        Thread(target=self.loadData, daemon=True).start()

    def loadData(self):
        if getEmployees():
            self.dataRows.extend(
                map(
                    lambda project: (
                        ProjectDataRow(
                            id=project.ID,
                            projectName=project.name,
                            startDate=project.startDate,
                            endDate=project.endDate,
                            status=project.status,
                            dataTable=self.dataTable
                        )
                    ),
                    getProjects()
                )
            )
        self.update()

    def sortProjectsList(self, sortCriteria: str = id):
        self.isAscendant = not self.isAscendant
        flag = self.isAscendant
        sortedProjects = getProjectsTableSorted(
            criteria=sortCriteria,
            sortMode="ASC" if flag else "DESC"
        )
        self.dataRows.clear()
        self.dataRows.extend(
            map(
                lambda project: (
                    ProjectDataRow(
                        id=project.ID,
                        projectName=project.name,
                        startDate=project.startDate,
                        endDate=project.endDate,
                        status=project.status,
                        dataTable=self.dataTable
                    )
                ),
                sortedProjects
            )
        )
        self.update()

    def showProjectDialog(self, e):
        addProjectDialog = AddProjectDialog(self)
        self.page.dialog = addProjectDialog
        addProjectDialog.open = True
        addProjectDialog.dialogEBAddProject.on_click = lambda _: self.addProject(
            projectName=addProjectDialog.dialogTFProjectName.value,
            startDate=addProjectDialog.selectedStartDate.value,
            endDate=addProjectDialog.selectedEndDate.value,
            status=addProjectDialog.selectedStatus
        )
        self.page.update()

    def addProject(self, projectName: str, startDate: str, endDate: str, status: str, ):
        if projectName and startDate and endDate and status:
            if createProject(Project(name=projectName, startDate=startDate, endDate=endDate, status=status)):
                self.dataRows.append(
                    ProjectDataRow(
                        id=getProjects()[-1].ID,
                        projectName=getProjects()[-1].name,
                        startDate=getProjects()[-1].startDate,
                        endDate=getProjects()[-1].endDate,
                        status=getProjects()[-1].status,
                        dataTable=self.dataTable
                    )
                )
            self.update()

    def searchProject(self, e):
        value = self.animatedSearchBar.getSearchEntry().lower()
        if value != "":
            filteredProject = filter(
                lambda project: (
                        str(project.ID).find(value) != -1
                        or project.name.lower().find(value) != -1
                        or project.startDate.lower().find(value) != -1
                        or project.endDate.lower().find(value) != -1
                        or project.status.lower().find(value) != -1
                ), getProjects()
            )
            self.dataRows.clear()
            self.dataRows.extend(
                map(
                    lambda project: ProjectDataRow(
                        id=project.ID,
                        projectName=project.name,
                        startDate=project.startDate,
                        endDate=project.endDate,
                        status=project.status,
                        dataTable=self.dataTable
                    ), filteredProject
                )
            )
        else:
            self.dataRows.clear()
            self.loadData()
        self.update()


# endregion

# region Camera
class Camera(Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.showCheckMessage = Text(
            color=colors.WHITE,
            font_family=str(PoppinsFont.MEDIUM),
        )
        self.content = Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.CENTER,
            spacing=15,
            controls=[
                ElevatedButton(
                    content=Text(
                        value="Check In",
                        color=colors.WHITE,
                        style=TextStyle(
                            font_family=str(PoppinsFont.MEDIUM)
                        ),
                    ), style=ButtonStyle(
                        shape=RoundedRectangleBorder(
                            radius=5
                        ),
                        bgcolor="#1D7D81",
                        overlay_color="#9cbab7"
                    ),
                    height=70,
                    width=150,
                    on_click=lambda _: Thread(target=self.checkIn).start()
                ),
                ElevatedButton(
                    content=Text(
                        value="Check Out",
                        color=colors.WHITE,
                        style=TextStyle(
                            font_family=str(PoppinsFont.MEDIUM)
                        ),
                    ),
                    style=ButtonStyle(
                        shape=RoundedRectangleBorder(
                            radius=5
                        ),
                        bgcolor="#1D7D81",
                        overlay_color="#9cbab7"
                    ),
                    height=70,
                    width=150,
                    on_click=lambda _: Thread(target=self.checkOut).start()
                ),
                self.showCheckMessage
            ]
        )

    # region loadEmployeesFaceEncodings
    @staticmethod
    def loadEmployeesFaceEncodings():
        employeeImages = getEmployeesImages()
        employeesFaceEncodings = []
        employeeIds = []
        for data in employeeImages:
            # Decode the base64 encoded image
            imageData = base64.b64decode(data["image"])
            # Convert bytes to numpy array
            npArray = np.frombuffer(imageData, np.uint8)
            # Decode numpy array to image
            employeeImage = cv2.imdecode(npArray, cv2.IMREAD_COLOR)
            # Get face encodings if a face is detected
            face_encodings = face_recognition.face_encodings(employeeImage)
            if face_encodings:
                faceEncoding = face_encodings[0]  # Take the first detected face
                employeesFaceEncodings.append(faceEncoding)
                employeeIds.append(data["id"])
            else:
                print("No face detected for employee with ID:", data["id"])
        return employeesFaceEncodings, employeeIds

    # endregion

    # region recognizeFaces
    # Function to recognize faces and return existence status, employee ID
    @staticmethod
    def recognizeFaces(rgb_image, image, known_face_encodings, employee_ids):
        face_locations = face_recognition.face_locations(rgb_image)
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Compare face encoding with the known face encodings
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            # If there is a match
            if True in matches:
                # Find the index of the matched face
                match_index = matches.index(True)
                cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
                # Get employee ID
                employee_id = employee_ids[match_index]
                return True, employee_id
            else:
                cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
        # If no match found
        return False, None

    # endregion

    # region Check In
    def checkIn(self):
        known_face_encodings, employee_ids = Camera.loadEmployeesFaceEncodings()
        # Initialize the camera
        cam = cv2.VideoCapture(0)
        # Set webcam resolution
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while True:
            # Read the input using the camera
            result, image = cam.read()

            # If image is detected without any error, proceed with face detection
            if result:
                # Convert the image to RGB format (required by face_recognition library)
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Detect faces and recognize
                exists, employee_id = Camera.recognizeFaces(rgb_image, image, known_face_encodings,
                                                            employee_ids)

                if exists:
                    Thread(target=scheduleCheckIn, args=[employee_id], daemon=True).start()
                    self.page.update()
                # Show the image
                cv2.imshow("Face Recognition", image)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # Close OpenCV windows
                cv2.destroyAllWindows()
                exit()

    # endregion

    # region check Out
    def checkOut(self):
        known_face_encodings, employee_ids = Camera.loadEmployeesFaceEncodings()
        # Initialize the camera
        cam = cv2.VideoCapture(0)
        # Set webcam resolution
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        while True:
            # Read the input using the camera
            result, image = cam.read()

            # If image is detected without any error, proceed with face detection
            if result:
                # Convert the image to RGB format (required by face_recognition library)
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Detect faces and recognize
                exists, employee_id = Camera.recognizeFaces(rgb_image, image, known_face_encodings,
                                                            employee_ids)

                if exists:
                    Thread(target=scheduleCheckOut, args=[employee_id], daemon=True).start()
                    self.page.update()
                # Show the image
                cv2.imshow("Face Recognition", image)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # Close OpenCV windows
                cv2.destroyAllWindows()
                exit()
    # endregion

# endregion
