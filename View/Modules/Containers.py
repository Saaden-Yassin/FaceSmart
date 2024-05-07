from PersonalControllers import *
from PersonalEnums import AppColors
from Controller.ManagerCRUD import *
from Controller.ScheduleCRUD import *


# region DashBoardContent
class DashBoardContent(Column):
    def __init__(self, col: int | float = None, username: str = "John Doe"):
        super().__init__()
        self.expand = True
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
                                                                    # text=,
                                                                    color="#1D7D81",
                                                                    content=Text(
                                                                        value="View All",
                                                                        size=16.1,
                                                                        weight=FontWeight.BOLD
                                                                    )
                                                                )
                                                            ]
                                                        ), Container(
                                                            margin=margin.only(top=25),
                                                            content=Column(
                                                                controls=[
                                                                    ProjectInfoContainer(
                                                                        progressValue=ProjectState.TESTING.value,
                                                                        progressBgColor="#172336",
                                                                        progressColor="#465F85",
                                                                        projectName="My Project FaceSmart",
                                                                        projectDaysLeft=7
                                                                    ),
                                                                    ProjectInfoContainer(
                                                                        progressValue=ProjectState.IN_PROGRESS.value,
                                                                        progressBgColor="#2B1D2C",
                                                                        progressColor="#844685",
                                                                        projectName="My Project FaceSmart",
                                                                        projectDaysLeft=7
                                                                    ),
                                                                    ProjectInfoContainer(
                                                                        progressValue=ProjectState.START.value,
                                                                        progressBgColor="#3F3023",
                                                                        progressColor="#C55D42",
                                                                        projectName="My Project FaceSmart",
                                                                        projectDaysLeft=7
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


# endregion

# region EmployeesList
class EmployeesList(Container):
    def __init__(self):
        super().__init__()
        self.padding = 16
        self.dataRows = []
        self.bgcolor = colors.TRANSPARENT
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
                        color="#C55D42",
                    ),
                ),
                DataColumn(
                    numeric=True,
                    label=TableHeadingContainer(
                        textValue="ID",
                        color="#C55D42",
                        enableSort=True,
                        onSortClick=lambda _: self.sortEmployeesList(sortCriteria="ID")
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="First name",
                        color="#C55D42",
                        enableSort=True,
                        onSortClick=lambda _: self.sortEmployeesList(sortCriteria="firstName")
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Last name",
                        color="#C55D42",
                        enableSort=True,
                        onSortClick=lambda _: self.sortEmployeesList(sortCriteria="lastName")
                    ),
                ),
                DataColumn(
                    numeric=True,
                    label=TableHeadingContainer(
                        textValue="Age",
                        color="#C55D42",
                        enableSort=True,
                        onSortClick=lambda _: self.sortEmployeesList(sortCriteria="age")
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Email",
                        color="#C55D42",
                        enableSort=True,
                        onSortClick=lambda _: self.sortEmployeesList(sortCriteria="email")
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Department",
                        color="#C55D42",
                        enableSort=True,
                        onSortClick=lambda _: self.sortEmployeesList(sortCriteria="departmentId"),
                        enableFilter=True,
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Current project",
                        color="#C55D42",
                        enableSort=True,
                        onSortClick=lambda _: self.sortEmployeesList(sortCriteria="projectId"),
                        enableFilter=True
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Status",
                        color="#C55D42",
                        enableFilter=True
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Delete",
                        color="#C55D42",
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
                                on_click=self.showDialog
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

    def showDialog(self, e):
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
        self.eb_login = self.login = ElevatedButton(
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
                color=colors.BLUE,
            ),
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=25),

            ),
            width=200,
            height=55,
        )
        self.t_managerNotExist = Text(
            color=colors.RED,
            font_family=str(PoppinsFont.MEDIUM_ITALIC),
        )
        self.rootPage = rootPage
        self.content = Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.CENTER,
            width=500,
            height=500,
            spacing=15,
            controls=[
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
                self.t_managerNotExist,
                ElevatedButton(
                    text="Go to home page ->",
                    on_click=lambda _: self.rootPage.go("/home"),
                )
            ]
        )

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
                self.page.go("/home")
            else:
                self.t_managerNotExist.value = "There is no manager with the given username and password !!!"
                self.t_managerNotExist.update()


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
        self.pickedEncodedImage = ""
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
                    side=BorderSide(width=1, color=colors.BLACK),
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
                self.eb_register
            ]
        )

    def validateRegister(self) -> bool:
        firstName = self.tf_managerFirstName.value
        lastName = self.tf_managerLastName.value
        username = self.tf_managerUsername.value
        password = self.tf_managerPassword.value
        age = self.tf_managerAge.value
        email = self.tf_managerEmail.value
        print("EImg -> ", self.pickedEncodedImage)
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
        return flag

    # endregion


# endregion

# region ManagerTransactions
class ManagerTransactions(Container):
    def __init__(self, rootPage: Page):
        super().__init__()
        self.alignment = alignment.center
        self.image_src = f"../assets/bgLeftNavBar.jpg"
        self.image_fit = ImageFit.COVER
        self.rootPage = rootPage
        self.expand = True
        self.managerLogin = ManagerLogin(
            bgColor=colors.with_opacity(opacity=0.7, color=colors.BLACK),
            rootPage=self.rootPage
        )
        self.managerLogin.eb_register.on_click = self.switchToRegister
        # self.managerLogin.eb_register.on_click = lambda _: self.rootPage.go("/home")
        self.managerRegister = ManagerRegister(
            rootPage=self.rootPage,
            bgColor=colors.with_opacity(opacity=0.7, color=colors.BLACK)
        )
        self.managerRegister.eb_register.on_click = self.switchToLogin
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

    def switchToLogin(self, e):
        if self.managerRegister.validateRegister():
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

# region Camera
class Camera(Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        # self.alignment = alignment.center
        self.content = Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                ElevatedButton(
                    content=Text(
                        value="Check In",
                        color=colors.WHITE,
                        style=TextStyle(
                            font_family=str(PoppinsFont.MEDIUM)
                        ),
                    ),
                    bgcolor="#1D7D81"
                ),
                ElevatedButton(
                    content=Text(
                        value="Check Out",
                        color=colors.WHITE,
                        style=TextStyle(
                            font_family=str(PoppinsFont.MEDIUM)
                        ),
                    ),
                    bgcolor="#1D7D81"
                ),
            ]
        )
# endregion
