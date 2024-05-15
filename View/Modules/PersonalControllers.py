import base64
import calendar
import concurrent.futures

import requests

from AnimatedControllers import *
from Controller.EmployeCRUD import *
from PersonalEnums import *
from View.Modules.Containers import EmployeesList, ProjectList


# region ProjectInfoContainer
class ProjectInfoContainer(Container):
    def __init__(self, progressValue: int | float | ProjectState = 50, progressBgColor: str = None,
                 progressColor: str = None,
                 projectName: str = None, projectDaysLeft: int = 0):
        super().__init__()
        self.border = border.all(width=2, color=colors.WHITE)
        self.border_radius = 15
        self.padding = padding.all(15)
        self.content = Row(
            controls=[
                AnimatedProgressRing(
                    col=1,
                    progressValue=progressValue,
                    bgColor=progressBgColor,
                    color=progressColor
                ),
                Text(
                    col=5,
                    value=projectName,
                    color=colors.WHITE,
                    font_family=str(PoppinsFont.MEDIUM)
                ),
                Row(
                    col=6,
                    alignment=MainAxisAlignment.END,
                    expand=True,
                    controls=[
                        Container(
                            col=1.5,
                            alignment=alignment.center,
                            bgcolor="#EEE6E2",
                            border_radius=5,
                            padding=padding.all(5),
                            content=Text(
                                font_family=str(PoppinsFont.REGULAR),
                                value=f"{projectDaysLeft} days left",
                                color=colors.BLACK,
                                # size=10
                            )
                        )
                    ]
                )
            ]
        )


# endregion

# region EmployeesCard
class EmployeesCard(Container):
    totalEmployees = 0

    def __init__(self, col: dict[str, int | float] | int | float = None, title: str = "Card title",
                 titleColor: str = None, iconName: str = icons.PEOPLE_ALT,
                 iconColor: str = None, shadowColor: str = None,
                 nbrEmployees: int = 100, totalEmployees: int = 100, progressIndicatorColor: str = None,
                 progressIndicatorBgColor: str = None, progressBarBgColor: str = None, progressBarColor: str = None):
        super().__init__()
        self.col = col
        self.border_radius = 55
        self.border = border.all(width=1, color=shadowColor)
        self.bgcolor = colors.BLACK
        self.height = 300
        self.shadow = BoxShadow(offset=Offset(x=-3, y=-3), color=shadowColor)
        self.alignment = alignment.center
        self.expand = True
        self.padding = padding.only(top=55, bottom=55, right=27, left=27)
        self.margin = margin.only(right=10)
        self.content = ResponsiveRow(
            controls=[
                Column(
                    spacing=25,
                    col=12,
                    controls=[
                        ResponsiveRow(
                            alignment=MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                Text(
                                    col=7,
                                    value=title,
                                    font_family=str(PoppinsFont.BOLD),
                                    color=titleColor,
                                    size=16.01
                                ),
                                Icon(
                                    col=2,
                                    size=30,
                                    name=iconName,
                                    color=iconColor
                                )
                            ]
                        ),
                        ResponsiveRow(
                            alignment=MainAxisAlignment.START,
                            controls=[
                                Text(
                                    col=12,
                                    size=25,
                                    value=str(nbrEmployees),
                                    weight=FontWeight.BOLD,
                                    color=colors.WHITE
                                ),
                            ]
                        ),
                        AnimatedProgressBar(
                            progressIndicatorBgColor=progressIndicatorBgColor,
                            progressIndicatorColor=progressIndicatorColor,
                            color=progressBarColor,
                            bgColor=progressBarBgColor,
                            nbrEmployees=nbrEmployees,
                            totalEmployees=EmployeesCard.totalEmployees
                        )
                    ]
                )
            ]
        )


# endregion

# region Calendar
cal = calendar.Calendar()

# Constants for day and month names
DAY_NAMES = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]


class Settings:
    """Settings for the calendar."""

    year: int = datetime.now().year
    month: int = datetime.now().month
    day: int = datetime.now().day

    @staticmethod
    def get_year() -> int:
        """Get the current year."""
        return Settings.year

    @staticmethod
    def get_month() -> int:
        """Get the current month."""
        return Settings.month

    @staticmethod
    def get_day() -> int:
        """Get the current day."""
        return Settings.day

    @staticmethod
    def get_date(delta: int):
        """Get the date with a delta change."""
        # Use modulus for handling month changes
        Settings.month = (Settings.month + delta - 1) % 12 + 1
        if delta > 0 and Settings.month == 1:
            Settings.year += 1
        elif delta < 0 and Settings.month == 12:
            Settings.year -= 1


class DateBox(Container):
    """Container to display a date box."""

    def __init__(
            self,
            day: int,
            date: str = None,
            date_instance: Column = None,
            opacity_: float | int = None,
    ):
        super().__init__()
        self.data = date
        self.opacity = opacity_
        self.width = 30
        self.height = 30
        self.alignment = alignment.center
        self.shape = BoxShape.RECTANGLE
        self.animate = Animation(duration=400, curve=AnimationCurve.EASE)
        self.border_radius = 5

        if day == Settings.get_day():
            self.selected()
        else:
            self.unselected()

        self.day = day
        self.date_instance = date_instance

        self.content = Text(
            value=str(self.day),
            text_align=alignment.center
        )

    def selected(self):
        """Apply selected style."""
        self.bgcolor = "#20303e"
        self.border = border.all(0.5, "#4fadf9")

    def unselected(self):
        """Apply unselected style."""
        self.bgcolor = None
        self.border = None


class DateGrid(Column):
    """Grid to display dates."""

    def __init__(self, year: int = datetime.year, month: int = datetime.month):
        super().__init__()
        self.year = year
        self.month = month
        self.date = Text(f"{MONTH_NAMES[self.month - 1]} {self.year}")
        self.controls = [
            Container(
                padding=padding.only(top=20),
                bgcolor=colors.BLACK,
                border_radius=border_radius.only(top_left=10, top_right=10),
                content=Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        IconButton(
                            icon="chevron_left",
                            on_click=lambda e: self.update_date_grid(e, -1)
                        ),
                        Container(
                            width=150,
                            content=self.date,
                            alignment=alignment.center
                        ),
                        IconButton(
                            icon="chevron_right",
                            on_click=lambda e: self.update_date_grid(e, 1)
                        ),
                    ],
                ),
            ),
            Row(
                alignment=MainAxisAlignment.SPACE_EVENLY,
                controls=[
                    DateBox(
                        day=DAY_NAMES[index],
                        opacity_=0.7
                    ) for index in range(7)
                ],
            )
        ]
        self.populate_date_grid(self.year, self.month)

    def populate_date_grid(self, year: int, month: int):
        """Populate the date grid."""
        # Clear existing rows after the day names row
        del self.controls[2:]
        for week in calendar.Calendar().monthdayscalendar(year, month):
            row = Row(alignment=MainAxisAlignment.SPACE_EVENLY)
            for day in week:
                if day != 0:
                    row.controls.append(
                        DateBox(
                            day, self.format_date(day),
                        )
                    )
                else:
                    row.controls.append(DateBox(" "))
            self.controls.append(row)

    def update_date_grid(self, e: TapEvent, delta: int):
        """Update the date grid."""
        Settings.get_date(delta)
        self.update_year_and_month(Settings.get_year(), Settings.get_month())
        self.populate_date_grid(Settings.get_year(), Settings.get_month())
        self.update()

    def update_year_and_month(self, year: int, month: int):
        """Update the year and month."""
        self.year = year
        self.month = month
        self.date.value = f"{MONTH_NAMES[self.month - 1]} {self.year}"

    def format_date(self, day: int) -> str:
        """Format the date."""
        return f"{MONTH_NAMES[self.month - 1]} {day}, {self.year}"


class Calendar(Container):
    """Container to display the calendar."""

    def __init__(self, col: int | float = None, padding_: int | float | Padding = None,
                 margin_: int | float | Margin = None, width: int | float = None, height: int | float = 350,
                 border_radius_: int | float | BorderRadius = None, bgcolor: str = None, opacity: Any = None,
                 alignment_: Alignment = None):
        super().__init__()
        self.height = height
        self.width = width
        self.opacity = opacity
        self.bgcolor = bgcolor
        self.border_radius = border_radius_
        self.padding = padding_
        self.margin = margin_
        self.clip_behavior = ClipBehavior.HARD_EDGE
        self.col = col
        self.alignment = alignment_
        self.content = DateGrid(
            year=Settings.get_year(),
            month=Settings.get_month()
        )
        # self.border = border.all(width=2, color=colors.WHITE)
        # self.border = border.only(BorderSide(width=2,color=colors.WHITE))


# endregion

# region EmployeesInOutContainer
class EmployeesInOutContainer(Container):
    def __init__(self, col: dict[str, int | float] | int | float = None, height: int | float | None = 300,
                 width: int | float = None,
                 circleImageBase64Src: str | bool | None = False,
                 circleImageSize: tuple[int, int] = (50, 50), employeeID: str | None = "ID value",
                 employeeName: str | None = "Employee name", hour: str | None = "00:00:00",
                 check: str | None = "checkOut"
                 ):
        super().__init__()
        self.col = col
        self.width = width
        self.height = height
        self.border_radius = 25
        self.padding = padding.all(15)
        self.border = border.all(width=2, color=colors.WHITE)
        self.bgcolor = colors.BLACK
        self.expand = True
        self.check = check
        self.hour = hour
        self.employeeName = employeeName
        self.employeeID = employeeID
        self.circleImageBase64Src = circleImageBase64Src
        self.content = Column(
            spacing=15,
            controls=[
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Text(
                            value="Check In/Out",
                            font_family=str(PoppinsFont.BOLD)
                        ),
                        ElevatedButton(
                            bgcolor=colors.TRANSPARENT,
                            content=Text(
                                value="View All",
                                color="#1D7D81",
                                size=14.1,
                                weight=FontWeight.BOLD,
                            )
                        )
                    ]
                ),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        CircleEmployeeImage(
                            height=circleImageSize[1],
                            width=circleImageSize[0],
                            imageSrcBase64=self.circleImageBase64Src,
                        )
                    ]
                ),
                Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        Text(
                            text_align=TextAlign.CENTER,
                            value=self.employeeName,
                            font_family=str(PoppinsFont.MEDIUM),
                            size=16.01
                        )

                    ]
                ),
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Text(
                            value="ID :",
                            font_family=str(PoppinsFont.MEDIUM),
                            size=16.01,
                        ),
                        Text(
                            value=self.employeeID,
                            font_family=str(PoppinsFont.BOLD),
                            size=16.01,
                        )

                    ]
                ),
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Text(
                            value="Hour :",
                            font_family=str(PoppinsFont.MEDIUM),
                            size=16.01,
                        ),
                        Text(
                            value=self.hour,
                            text_align=TextAlign.END,
                            font_family=str(PoppinsFont.BOLD),
                            size=16.01,
                        )
                    ]
                ),
                Row(
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        Text(
                            value="Status :",
                            font_family=str(PoppinsFont.MEDIUM),
                            size=16.01,
                        ),
                        Container(
                            padding=padding.all(5),
                            bgcolor="#B5FF57" if self.check == "checkIn" else colors.RED,
                            border_radius=10,
                            content=Text(
                                value=self.check,
                                color=colors.BLACK,
                                font_family=str(PoppinsFont.BOLD),
                                size=16.01,
                            )
                        )
                    ]
                )
            ]
        )


# endregion

# region DashBoardImage
class DashBoardImage(Container):
    def __init__(self, username: str):
        super().__init__()
        self.userText = TypeWriter(
            displayedText=f"Hi, {username}",
            color=colors.BLACK,
            font_family=str(PoppinsFont.MEDIUM),
            size=17,

        )
        self.welcomingText = TypeWriter(
            displayedText="Welcome to Face Smart",
            color=colors.BLACK,
            weight=FontWeight.BOLD,
            size=37,
        )
        self.quoteText = Container(
            margin=margin.only(top=5),
            content=TypeWriter(
                displayedText="Loading quote...",
                color=colors.BLACK,
                font_family=str(PoppinsFont.MEDIUM_ITALIC),
                size=15,
                width=650,
            )
        )
        self.textColumn = Column(
            left=380,
            top=110,
            spacing=0,
        )
        self.content = Stack(
            expand=True,
            controls=[
                ResponsiveRow(
                    controls=[
                        Image(
                            src=f"../assets/HomeImage.png",
                        )
                    ]
                ),
                self.textColumn
            ]
        )

    def did_mount(self):
        Thread(target=self.showText, daemon=True).start()
        Thread(target=self.__quoteThreadLoop, daemon=True).start()

    def __quoteThreadLoop(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(DashBoardImage.__fetch_quote)
            result = future.result()

            if len(self.textColumn.controls) > 2:
                self.textColumn.controls.pop()
                self.textColumn.controls.append(
                    Container(
                        margin=margin.only(top=5),
                        content=TypeWriter(
                            displayedText=f"{result[0]}\nAuthor : {result[1]}",
                            color=colors.BLACK,
                            font_family=str(PoppinsFont.MEDIUM_ITALIC),
                            size=15,
                            width=650,
                        )
                    )
                )
                self.textColumn.update()

    def showText(self):
        self.textColumn.controls.append(self.userText)
        self.textColumn.update()
        sleep(1.5)
        self.textColumn.controls.append(self.welcomingText)
        self.textColumn.update()
        sleep(0.68)
        self.textColumn.controls.append(self.quoteText)
        self.textColumn.update()

    @staticmethod
    def __fetch_quote() -> tuple[str, str]:
        data = DashBoardImage.__fetch_data()
        while len(data[0].get('quote')) > 80:
            data = DashBoardImage.__fetch_data()
        else:
            quote, author = data[0].get('quote'), data[0].get('author')
        return quote, author

    @staticmethod
    def __fetch_data() -> Any:
        try:
            category = 'leadership'
            api_url = f'https://api.api-ninjas.com/v1/quotes?category={category}'
            response = requests.get(api_url, headers={'X-Api-Key': 'gQR91b8x9JaadnJi+offIQ==7M4J8SLHl9cyDVVz'})
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            if data:
                return data
            else:
                return False
        except requests.exceptions.RequestException as e:
            print("Error fetching data:", e)
            return "", ""
        except ValueError as e:
            print("Error parsing JSON:", e)
            return "", ""


# endregion

# region TableHeadingContainer
class TableHeadingContainer(Container):
    def __init__(self, textValue: str = "header", color: str = None, enableSort: bool = False,
                 enableFilter: bool = False, onSortClick: Any = None):
        super().__init__()
        self.content = Row(
            alignment=MainAxisAlignment.CENTER,
            width=250,
            spacing=3,
            controls=[
                Row(
                    controls=[
                        Text(
                            value=f"{textValue}",
                            color=color,
                            size=16.1,
                            font_family=str(PoppinsFont.BOLD),
                        ),
                        IconButton(
                            icon=icons.SORT_BY_ALPHA_ROUNDED,
                            icon_size=16.1,
                            visible=enableSort,
                            on_click=onSortClick
                        ),
                        IconButton(
                            icon=icons.ARROW_DROP_DOWN,
                            icon_size=19.1,
                            visible=enableFilter
                        )
                    ]
                )
            ]
        )


# endregion

# region LeftNavigationBar
class LeftNavigationBar(NavigationRail):
    def __init__(self):
        super().__init__()
        self.col = 2.3,
        self.selected_index = 0
        self.indicator_color = colors.BLUE
        self.label_type = NavigationRailLabelType.ALL
        self.min_width = 100
        self.extended = True
        self.expand = True
        self.group_alignment = -0.7
        self.bgcolor = colors.TRANSPARENT
        self.leading = Image(
            src=f"../assets/navbarLogo.png"
        )
        self.destinations = [
            NavigationRailDestination(
                icon=icons.DASHBOARD,
                label_content=Text(
                    value="Dashboard",
                    size=18
                ),
                padding=padding.only(bottom=25)

            ),
            NavigationRailDestination(
                icon=icons.GROUPS_ROUNDED,
                label_content=Text(
                    value="Employees",
                    size=18
                ),
                padding=padding.only(bottom=25)
            ),
            NavigationRailDestination(
                icon=icons.PENDING_ACTIONS_ROUNDED,
                label_content=Text(
                    value="Projects",
                    size=18
                ),
                padding=padding.only(bottom=25)
            ),
            NavigationRailDestination(
                icon=icons.APARTMENT_ROUNDED,
                label_content=Text(
                    value="Departments",
                    size=18
                ),
                padding=padding.only(bottom=25)
            ),
            NavigationRailDestination(
                icon=icons.NOTIFICATIONS_ON_ROUNDED,
                label_content=Text(
                    value="Notifications",
                    size=18
                ),
                padding=padding.only(bottom=25)
            ),
            NavigationRailDestination(
                icon=icons.CAMERA_ROUNDED,
                label_content=Text(
                    value="Camera",
                    size=18
                ),
                padding=padding.only(bottom=25)
            ),
            NavigationRailDestination(
                icon=icons.LOGOUT_ROUNDED,
                label_content=Text(
                    value="Logout",
                    size=18
                )
            ),
        ]


# endregion

# region AddEmployeeDialog
class AddEmployeeDialog(AlertDialog):
    def __init__(self, employeesList: EmployeesList):
        super().__init__()
        self.modal = True
        self.shadow_color = colors.BLACK
        self.content_padding = 0
        self.actions_padding = 0
        self.employeesList = employeesList
        self.selectedDepartment: str = ""
        self.dialogImage = Image(
            src=f"../assets/eye.png",
            width=120,
            height=120,
        )
        self.dialogTFFirstName = TextField(
            label="First name",
            border_radius=15,
            text_style=TextStyle(font_family=str(PoppinsFont.MEDIUM))
        )
        self.dialogTFLastName = TextField(
            label="Last name",
            border_radius=15,
            text_style=TextStyle(font_family=str(PoppinsFont.MEDIUM))
        )
        self.dialogTFAge = TextField(
            label="Age",
            border_radius=15,
            text_style=TextStyle(font_family=str(PoppinsFont.MEDIUM)),

        )
        self.dialogTFEmail = TextField(
            label="Email",
            border_radius=15,
            text_style=TextStyle(font_family=str(PoppinsFont.MEDIUM))
        )
        self.dialogTFCurrentProject = TextField(
            label="Current project",
            border_radius=15,
            text_style=TextStyle(font_family=str(PoppinsFont.MEDIUM))
        )
        self.dialogDDDepartment = Dropdown(
            alignment=alignment.top_right,
            label="Department",
            border_radius=15,
            bgcolor="#173839",
            options=[
                dropdown.Option(key="HR"),
                dropdown.Option(key="Computer science"),
                dropdown.Option(key="Marketing")
            ],
            on_change=self.selectDepartment
        )
        self.imageSelectedMsg = Text(
            font_family=str(PoppinsFont.BOLD_ITALIC),
            size=13
        )
        self.dialogEBAddEmployee = ElevatedButton(
            content=Text(
                value="Add",
                size=16.1,
                font_family=str(PoppinsFont.BOLD)
            ),
            bgcolor="#173839",
            color=colors.WHITE,
            width=100,
            height=50,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=10)
            ),
        )
        self.localImagePicker = LocalImagePicker(
            rootPage=self.employeesList.page,
            btnPickImage=FilledButton(
                content=Row(
                    controls=[
                        Icon(
                            name=icons.UPLOAD_FILE_ROUNDED,
                            color=colors.WHITE
                        ),
                        Text(
                            value="Click to upload image",
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
            showPickedImageName=self.imageSelectedMsg,
        )
        self.content = Column(
            scroll=ScrollMode.ALWAYS,
            controls=[
                Container(
                    padding=padding.all(16),
                    border_radius=30,
                    gradient=AppColors.BLACK_GREEN_LINEAR_GRADIAN.value,
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        spacing=15,
                        controls=[
                            self.dialogImage,
                            self.dialogTFFirstName,
                            self.dialogTFLastName,
                            self.dialogTFAge,
                            self.dialogTFEmail,
                            self.dialogDDDepartment,
                            self.dialogTFCurrentProject,
                            self.localImagePicker,
                            Row(
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    self.dialogEBAddEmployee,
                                    ElevatedButton(
                                        content=Text(
                                            value="Close",
                                            size=16.1,
                                            font_family=str(PoppinsFont.BOLD)
                                        ),
                                        bgcolor=colors.TRANSPARENT,
                                        color=colors.GREY,
                                        height=50,
                                        style=ButtonStyle(
                                            shape=RoundedRectangleBorder(radius=10)
                                        ),
                                        on_click=self.closeDialog
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        )

    def selectDepartment(self, e):
        self.selectedDepartment = self.dialogDDDepartment.value

    def closeDialog(self, e):
        self.open = False
        self.employeesList.page.update()


# endregion

# region CircleEmployeeImage
class CircleEmployeeImage(Container):
    def __init__(self, imageSrcBase64: str | bool = False, width: int | float = 45, height: int | float = 45):
        super().__init__()
        if not imageSrcBase64:
            self.image_src = f"../assets/profile.jpg"
        else:
            self.image_src_base64 = imageSrcBase64
        self.image_repeat = ImageRepeat.NO_REPEAT
        self.image_fit = ImageFit.COVER
        self.width = width
        self.height = height
        self.border_radius = 40


# endregion

# region EmployeeDataRow
class EmployeeDataRow(DataRow):
    def __init__(self, id: int, imageSrcBase64: base64, firstName: str, lastName: str, age: int,
                 email: str, department: str,
                 status: str,
                 currentProject: str = "Current project", dataTable: DataTable = None):
        super().__init__()
        self.dataTable = dataTable
        self.t_id = Text(
            value=str(id),
            font_family=str(PoppinsFont.MEDIUM),
            width=250,
            text_align=TextAlign.CENTER,
        )
        self.tf_firstName = TextField(
            value=firstName,
            width=250,
            text_align=TextAlign.CENTER,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM)
            ),
            color=colors.WHITE,
            border_width=0,
            disabled=True
        )
        self.tf_lastName = TextField(
            value=lastName,
            width=250,
            text_align=TextAlign.CENTER,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM)
            ),
            color=colors.WHITE,
            border_width=0,
            disabled=True
        )
        self.tf_age = TextField(
            value=str(age),
            width=250,
            text_align=TextAlign.CENTER,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM)
            ),
            color=colors.WHITE,
            border_width=0,
            disabled=True
        )
        self.tf_email = TextField(
            value=email,
            width=250,
            text_align=TextAlign.CENTER,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM)
            ),
            color=colors.WHITE,
            border_width=0,
            disabled=True
        )
        self.tf_department = TextField(
            value=department,
            width=250,
            text_align=TextAlign.CENTER,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM)
            ),
            color=colors.WHITE,
            border_width=0,
            disabled=True
        )
        self.tf_currentProject = TextField(
            value=currentProject,
            width=250,
            text_align=TextAlign.CENTER,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM)
            ),
            color=colors.WHITE,
            border_width=0,
            disabled=True
        )
        self.t_status = Text(
            value=status,
            width=250,
            text_align=TextAlign.CENTER,
            font_family=str(PoppinsFont.MEDIUM)
        )
        self.cells = [
            DataCell(
                content=Container(
                    alignment=alignment.center,
                    content=Row(
                        alignment=MainAxisAlignment.CENTER,
                        controls=[
                            CircleEmployeeImage(
                                imageSrcBase64=imageSrcBase64
                            )
                        ]
                    )
                ),
            ),
            DataCell(
                content=self.t_id,
            ),
            DataCell(
                content=self.tf_firstName,
                on_tap=self.updateFirstName,
            ),
            DataCell(
                content=self.tf_lastName,
                on_tap=self.updateLastName,
            ),
            DataCell(
                content=self.tf_age,
                on_tap=self.updateAge,
            ),
            DataCell(
                content=self.tf_email,
                on_tap=self.updateEmail,
            ),
            DataCell(
                content=self.tf_department,
                on_tap=self.updateDepartment,
            ),
            DataCell(
                content=self.tf_currentProject,
                on_tap=self.updateProjectName,
            ),
            DataCell(
                content=self.t_status
            ),
            DataCell(
                content=Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        IconButton(
                            icon=icons.DELETE_ROUNDED,
                            icon_color=colors.RED,
                            on_click=self.deleteEmployee
                        )
                    ]
                )
            )
        ]

    # region FirstName
    def updateFirstName(self, e):
        self.tf_firstName.disabled = False
        self.tf_firstName.value = ""
        self.tf_firstName.hint_text = "Enter new first name..."
        self.tf_firstName.border_width = 1
        self.tf_firstName.on_submit = self.updateEffectFirstName
        self.tf_firstName.update()

    def updateEffectFirstName(self, e):
        updateEmployee(ID=int(self.t_id.value), firstName=self.tf_firstName.value)
        self.tf_firstName.border_width = 0
        self.tf_firstName.update()

    # endregion

    # region LastName
    def updateLastName(self, e):
        self.tf_lastName.disabled = False
        self.tf_lastName.value = ""
        self.tf_lastName.hint_text = "Enter new last name..."
        self.tf_lastName.border_width = 1
        self.tf_lastName.on_submit = self.updateEffectLastName
        self.tf_lastName.update()

    def updateEffectLastName(self, e):
        updateEmployee(ID=int(self.t_id.value), lastName=self.tf_lastName.value)
        self.tf_lastName.border_width = 0
        self.tf_lastName.update()

    # endregion

    # region Age
    def updateAge(self, e):
        self.tf_age.disabled = False
        self.tf_age.value = ""
        self.tf_age.hint_text = "Enter new age..."
        self.tf_age.border_width = 1
        self.tf_age.on_submit = self.updateEffectAge
        self.tf_age.update()

    def updateEffectAge(self, e):
        updateEmployee(ID=int(self.t_id.value), age=int(self.tf_age.value))
        self.tf_age.border_width = 0
        self.tf_age.update()

    # endregion

    # region Email
    def updateEmail(self, e):
        self.tf_email.disabled = False
        self.tf_email.value = ""
        self.tf_email.hint_text = "Enter new email..."
        self.tf_email.border_width = 1
        self.tf_email.on_submit = self.updateEffectEmail
        self.tf_email.update()

    def updateEffectEmail(self, e):
        updateEmployee(ID=int(self.t_id.value), email=self.tf_email.value)
        self.tf_email.border_width = 0
        self.tf_email.update()

    # endregion

    # region Department
    def updateDepartment(self, e):
        self.tf_department.disabled = False
        self.tf_department.value = ""
        self.tf_department.hint_text = "Enter new department..."
        self.tf_department.border_width = 1
        self.tf_department.on_submit = self.updateEffectDepartment
        self.tf_department.update()

    def updateEffectDepartment(self, e):
        updateEmployee(ID=int(self.t_id.value), departmentName=self.tf_department.value)
        self.tf_department.border_width = 0
        self.tf_department.update()

    # endregion

    # region Current Project
    def updateProjectName(self, e):
        self.tf_currentProject.disabled = False
        self.tf_currentProject.value = ""
        self.tf_currentProject.hint_text = "Enter new current project..."
        self.tf_currentProject.border_width = 1
        self.tf_currentProject.on_submit = self.updateEffectProjectName
        self.tf_currentProject.update()

    def updateEffectProjectName(self, e):
        updateEmployee(ID=int(self.t_id.value), projectName=self.tf_currentProject.value)
        self.tf_currentProject.border_width = 0
        self.tf_currentProject.update()

    # endregion

    def deleteEmployee(self, e):
        deleteEmployee(ID=int(self.t_id.value))
        self.dataTable.rows.remove(self)
        self.dataTable.update()


# endregion

# region LocalImagePicker
class LocalImagePicker(Container):
    def __init__(self, rootPage: Page, btnPickImage: FilledButton, showPickedImageName: Text,
                 margin_: int | float | Margin = None):
        super().__init__()
        self.rootPage = rootPage
        self.margin = margin_
        self.showPickedImageName = showPickedImageName
        self.btnPickImage = btnPickImage
        self.pickedEncodedImage: str = ""
        self.selectedDepartment: str = ""
        self.pickImageDialog = FilePicker(on_result=self.pickImage)
        if self.rootPage:
            self.rootPage.overlay.append(self.pickImageDialog)
            self.rootPage.update()
        self.btnPickImage.on_click = lambda _: self.pickImageDialog.pick_files()
        self.content = Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                self.btnPickImage,
                self.showPickedImageName
            ]
        )

    def pickImage(self, e: FilePickerResultEvent):
        if not e.files == "":
            try:
                with open(e.files[0].path, "rb") as image_file:
                    self.pickedEncodedImage = base64.b64encode(image_file.read()).decode()
                    self.showPickedImageName.value = e.files[0].name
            except Exception as e:
                print(e)
                print("YOU HAVE PROBLEM HERE !!!!")
        else:
            self.showPickedImageName.value = "Image not found !!!"
        self.showPickedImageName.update()

    def getPickedEncodedImage(self):
        if self.pickedEncodedImage:
            return self.pickedEncodedImage
        return ""


# endregion

# region AddProjectDialog
class AddProjectDialog(AlertDialog):
    def __init__(self, projectList: ProjectList):
        super().__init__()
        self.modal = True
        self.shadow_color = colors.BLACK
        self.content_padding = 0
        self.actions_padding = 0
        self.projectList = projectList
        self.selectedStatus: str = ""
        self.selectedStartDate: str = ""
        self.selectedEndDate: str = ""
        self.dialogImage = Image(
            src=f"../assets/eye.png",
            width=120,
            height=120,
        )
        self.dialogTFProjectName = TextField(
            label="Project name",
            border_radius=15,
            text_style=TextStyle(font_family=str(PoppinsFont.MEDIUM))
        )
        self.dialogDPStartDate = DatePicker(
            on_change=self.onChangeStartDate,
            current_date=datetime.now(),
        )
        self.projectList.page.overlay.append(self.dialogDPStartDate)

        self.dialogDPEndDate = DatePicker(
            on_change=self.onChangeEndDate,
            current_date=datetime.now(),
        )
        self.projectList.page.overlay.append(self.dialogDPEndDate)

        self.stateOptions = []
        for state in ProjectState:
            self.stateOptions.append(dropdown.Option(key=state.name))

        self.dialogDDStatus = Dropdown(
            alignment=alignment.top_right,
            label="Status",
            border_radius=15,
            bgcolor="#173839",
            options=self.stateOptions,
            on_change=self.selectDepartment
        )
        self.dialogEBAddProject = ElevatedButton(
            content=Text(
                value="Add",
                size=16.1,
                font_family=str(PoppinsFont.BOLD)
            ),
            bgcolor="#173839",
            color=colors.WHITE,
            width=100,
            height=50,
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=10)
            ),
        )
        self.content = Column(
            scroll=ScrollMode.ALWAYS,
            controls=[
                Container(
                    padding=padding.all(16),
                    border_radius=30,
                    gradient=AppColors.BLACK_GREEN_LINEAR_GRADIAN.value,
                    content=Column(
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                        spacing=15,
                        controls=[
                            self.dialogImage,
                            self.dialogTFProjectName,
                            FilledButton(
                                content=Row(
                                    controls=[
                                        Icon(
                                            name=icons.CALENDAR_MONTH,
                                            color=colors.WHITE
                                        ),
                                        Text(
                                            value="Pick start date",
                                            font_family=str(PoppinsFont.BOLD),
                                            color=colors.WHITE
                                        )
                                    ]
                                ),
                                on_click=lambda _: self.dialogDPStartDate.pick_date(),
                                height=55,
                                style=ButtonStyle(
                                    bgcolor=colors.TRANSPARENT,
                                    shape=RoundedRectangleBorder(radius=15),
                                    side=BorderSide(width=1, color=colors.BLACK),
                                )
                            ),
                            FilledButton(
                                content=Row(
                                    controls=[
                                        Icon(
                                            name=icons.CALENDAR_MONTH,
                                            color=colors.WHITE
                                        ),
                                        Text(
                                            value="Pick end date",
                                            font_family=str(PoppinsFont.BOLD),
                                            color=colors.WHITE
                                        )
                                    ]
                                ),
                                on_click=lambda _: self.dialogDPEndDate.pick_date(),
                                height=55,
                                style=ButtonStyle(
                                    bgcolor=colors.TRANSPARENT,
                                    shape=RoundedRectangleBorder(radius=15),
                                    side=BorderSide(width=1, color=colors.BLACK),
                                )
                            ),
                            self.dialogDDStatus,
                            Row(
                                alignment=MainAxisAlignment.CENTER,
                                controls=[
                                    self.dialogEBAddProject,
                                    ElevatedButton(
                                        content=Text(
                                            value="Close",
                                            size=16.1,
                                            font_family=str(PoppinsFont.BOLD)
                                        ),
                                        bgcolor=colors.TRANSPARENT,
                                        color=colors.GREY,
                                        height=50,
                                        style=ButtonStyle(
                                            shape=RoundedRectangleBorder(radius=10)
                                        ),
                                        on_click=self.closeDialog
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        )

    def selectDepartment(self, e):
        self.selectedStatus = self.dialogDDStatus.value

    def onChangeStartDate(self, e):
        self.selectedStartDate = self.dialogDPStartDate.value.strftime("%Y-%m-%d")

    def onChangeEndDate(self, e):
        self.selectedEndDate = self.dialogDPEndDate.value.strftime("%Y-%m-%d")

    def closeDialog(self, e):
        self.open = False
        self.projectList.page.update()


# endregion

# region ProjectDataRow
class ProjectDataRow(DataRow):
    def __init__(self, id: int, projectName: str, startDate: str,
                 endDate: str, status: str, dataTable: DataTable = None):
        super().__init__()
        self.dataTable = dataTable
        self.t_id = Text(
            value=str(id),
            font_family=str(PoppinsFont.MEDIUM),
            width=250,
            text_align=TextAlign.CENTER,
        )
        self.tf_projectName = TextField(
            value=projectName,
            width=250,
            text_align=TextAlign.CENTER,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM)
            ),
            color=colors.WHITE,
            border_width=0,
            disabled=True
        )
        self.tf_startDate = TextField(
            value=startDate,
            width=250,
            text_align=TextAlign.CENTER,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM)
            ),
            color=colors.WHITE,
            border_width=0,
            disabled=True
        )
        self.tf_endDate = TextField(
            value=endDate,
            width=250,
            text_align=TextAlign.CENTER,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM)
            ),
            color=colors.WHITE,
            border_width=0,
            disabled=True
        )
        self.tf_status = TextField(
            value=status,
            width=250,
            text_align=TextAlign.CENTER,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM)
            ),
            color=colors.WHITE,
            border_width=0,
            disabled=True
        )
        self.cells = [
            DataCell(
                content=self.t_id,
            ),
            DataCell(
                content=self.tf_projectName,
                on_tap=self.updateProjectName,
            ),
            DataCell(
                content=self.tf_startDate,
                on_tap=self.updateStartDate,
            ),
            DataCell(
                content=self.tf_endDate,
                on_tap=self.updateEndDate,
            ),
            DataCell(
                content=self.tf_status,
                on_tap=self.updateStatus,
            ),
            DataCell(
                content=Row(
                    alignment=MainAxisAlignment.CENTER,
                    controls=[
                        IconButton(
                            icon=icons.DELETE_ROUNDED,
                            icon_color=colors.RED,
                            on_click=self.deleteProject
                        )
                    ]
                )
            )
        ]

    # region Project
    def updateProjectName(self, e):
        self.tf_projectName.disabled = False
        self.tf_projectName.value = ""
        self.tf_projectName.hint_text = "Enter new project name..."
        self.tf_projectName.border_width = 1
        self.tf_projectName.on_submit = self.updateEffectProjectName
        self.tf_projectName.update()

    def updateEffectProjectName(self, e):
        updateProject(ID=int(self.t_id.value), name=self.tf_projectName.value)
        self.tf_projectName.border_width = 0
        self.tf_projectName.update()

    # endregion

    # region Start date
    def updateStartDate(self, e):
        self.tf_startDate.disabled = False
        self.tf_startDate.value = ""
        self.tf_startDate.hint_text = "Enter new start date..."
        self.tf_startDate.border_width = 1
        self.tf_startDate.on_submit = self.updateEffectStartDate
        self.tf_startDate.update()

    def updateEffectStartDate(self, e):
        updateProject(ID=int(self.t_id.value), startDate=self.tf_startDate.value)
        self.tf_startDate.border_width = 0
        self.tf_startDate.update()

    # endregion

    # region End date
    def updateEndDate(self, e):
        self.tf_endDate.disabled = False
        self.tf_endDate.value = ""
        self.tf_endDate.hint_text = "Enter new end date..."
        self.tf_endDate.border_width = 1
        self.tf_endDate.on_submit = self.updateEffectEndDate
        self.tf_endDate.update()

    def updateEffectEndDate(self, e):
        updateProject(ID=int(self.t_id.value), endDate=self.tf_endDate.value)
        self.tf_endDate.border_width = 0
        self.tf_endDate.update()

    # endregion

    # region Status
    def updateStatus(self, e):
        self.tf_status.disabled = False
        self.tf_status.value = ""
        self.tf_status.hint_text = "Enter new status..."
        self.tf_status.border_width = 1
        self.tf_status.on_submit = self.updateEffectStatus
        self.tf_status.update()

    def updateEffectStatus(self, e):
        updateProject(ID=int(self.t_id.value), status=self.tf_status.value)
        self.tf_status.border_width = 0
        self.tf_status.update()

    # endregion

    def deleteProject(self, e):
        deleteProject(ID=int(self.t_id.value))
        self.dataTable.rows.remove(self)
        self.dataTable.update()

# endregion
