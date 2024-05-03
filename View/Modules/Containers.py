from Controller.EmployeCRUD import *
from PersonalControllers import *
from PersonalEnums import AppColors


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
                                                                nbrEmployees=1500,
                                                                totalEmployees=1500,
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
                                                                nbrEmployees=1000,
                                                                totalEmployees=1500,
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
                                                                nbrEmployees=500,
                                                                totalEmployees=1500,
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
                                            col=3
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
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="First name",
                        color="#C55D42",
                        enableSort=True,
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Last name",
                        color="#C55D42",
                        enableSort=True,
                    ),
                ),
                DataColumn(
                    numeric=True,
                    label=TableHeadingContainer(
                        textValue="Age",
                        color="#C55D42",
                        enableSort=True,
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Email",
                        color="#C55D42",
                        enableSort=True,
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Department",
                        color="#C55D42",
                        enableSort=True,
                        enableFilter=True
                    ),
                ),
                DataColumn(
                    label=TableHeadingContainer(
                        textValue="Current project",
                        color="#C55D42",
                        enableSort=True,
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
                            # expand=True,
                            scroll=ScrollMode.ADAPTIVE,
                            controls=[
                                self.dataTable
                            ]
                        )
                    ]
                )
            ]
        )

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
            image=addEmployeeDialog.pickedEncodedImage,
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
                        or emp.departmentName.lower().find(value) != -1
                        or emp.projectName.lower().find(value) != -1
                        or emp.status.lower().find(value) != -1
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
        self.update()


# endregion


# region ManagerLogin
class ManagerLogin(Container):
    def __init__(self, bgColor: str = None):
        super().__init__()
        self.bgcolor = bgColor
        self.width = 500
        self.padding = padding.only(left=18, right=18)
        self.border_radius = 40
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
        self.content = Column(
            width=500,
            height=500,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.CENTER,
            controls=[
                Image(
                    src=f"../assets/eye.png",
                ),
                Text(
                    value="Login",
                    text_align=TextAlign.CENTER,
                    size=30,
                ),
                Container(
                    margin=margin.only(bottom=15),
                    content=self.tf_managerUsername,
                ),
                Container(
                    margin=margin.only(bottom=15),
                    content=self.tf_managerPassword,
                ),
                ElevatedButton(
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
                    width=500,
                    height=55,
                    on_click=self.checkIfEmptyOrBlank,
                )
            ]
        )

    def checkIfEmptyOrBlank(self, e):
        username = self.tf_managerUsername.value
        password = self.tf_managerPassword.value

        if not (username and password):
            if not username:
                self.tf_managerUsername.error_text = "Missing username"
                self.tf_managerUsername.update()
            else:
                self.tf_managerUsername.error_text = ""
                self.tf_managerUsername.update()
            if not password:
                self.tf_managerPassword.error_text = "Missing password"
                self.tf_managerPassword.update()
            else:
                self.tf_managerPassword.error_text = ""
                self.tf_managerPassword.update()
        else:
            self.page.go("/home")


# endregion


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


