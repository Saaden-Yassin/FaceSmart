from threading import Thread
from time import sleep
from typing import Any
from flet import *
from PersonalEnums import PoppinsFont


# region AnimatedProgressRing
class AnimatedProgressRing(Stack):
    def __init__(self, progressValue: int | float = 50, width: int | float = 60, height: int | float = 60,
                 barWidth: int | float = 6, bgColor: str = None, color: str = None,
                 col: dict[str, int | float] | int | float = None):
        super().__init__()
        self.progressValue = progressValue
        self.progressRing = ProgressRing(
            width=width,
            height=height,
            stroke_width=barWidth,
            bgcolor=bgColor,
            color=color,
            stroke_cap=StrokeCap.ROUND,
            stroke_align=-1.0,
        )
        self.col = col
        self.controls = [
            self.progressRing,
            Text(
                top=17,
                left=14,
                value=f"{str(progressValue)}%",
                size=16,
                weight=FontWeight.W_500
            )
        ]

    def did_mount(self):
        Thread(target=self.animateProgress, daemon=True).start()

    def animateProgress(self):
        for i in range(0, self.progressValue):
            self.progressRing.value = i * 0.01
            sleep(0.030)
            self.progressRing.update()


# endregion

# region AnimatedProgressBar
class AnimatedProgressBar(Column):
    def __init__(self, barHeight: int | float = 15, bgColor: str = None, color: str = None,
                 progressIndicatorColor: str = None, progressIndicatorBgColor: str = None,
                 nbrEmployees: int = 100, totalEmployees: int = 100,
                 col: dict[str, int | float] | int | float = None):
        super().__init__()
        self.__nbrEmployees = nbrEmployees
        self.__totalEmployees = totalEmployees
        self.col = col
        self.progressBar = ProgressBar(
            bar_height=barHeight,
            color=color,
            border_radius=25,
            bgcolor=bgColor
        )
        self.controls = [
            self.progressBar,
            Container(
                alignment=alignment.top_right,
                content=Container(
                    alignment=alignment.center,
                    width=50,
                    bgcolor=progressIndicatorBgColor,
                    margin=margin.only(right=22),
                    border_radius=7,
                    content=Text(
                        value=f"{str(self.percentageProgressValue())}%",
                        size=15,
                        weight=FontWeight.BOLD,
                        color=progressIndicatorColor,
                    )
                )
            )
        ]

    @property
    def nbrEmployees(self):
        return self.__nbrEmployees

    @property
    def totalEmployees(self):
        return self.__totalEmployees

    def percentageProgressValue(self) -> int:
        return round((self.nbrEmployees / self.totalEmployees) * 100)

    def did_mount(self):
        Thread(target=self.animateProgress, daemon=True).start()

    def animateProgress(self):
        for i in range(0, self.percentageProgressValue() + 1):
            self.progressBar.value = i * 0.01
            sleep(0.030)
            self.progressBar.update()


# endregion

# region TypeWriter
class TypeWriter(Text):
    def __init__(self, displayedText: str, font_family: str = None, color: str = None, size: int | float = None,
                 weight: FontWeight = None, opacity: Any = None, width: int | float = None, no_wrap: bool = False):
        super().__init__()
        self.displayedText = displayedText
        self.font_family = font_family
        self.color = color
        self.size = size
        self.no_wrap = no_wrap
        self.weight = weight
        self.opacity = opacity
        self.width = width

    def did_mount(self):
        Thread(target=self.effect, daemon=True).start()

    def effect(self):
        self.value = ""
        for i in range(len(self.displayedText)):
            self.value += self.displayedText[i]
            self.update()
            sleep(0.05)


# endregion

# region AnimatedSearchBar
class AnimatedSearchBar(Container):
    def __init__(self):
        super().__init__()
        # self.loadDataFunc: () = None
        self.__searchEntry = TextField(
            hint_text="Search record",
            hint_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM),
            ),
            border_width=0,
            width=0,
            text_style=TextStyle(
                font_family=str(PoppinsFont.MEDIUM)
            ),
            animate_size=Animation(
                duration=1000,
                curve=AnimationCurve.EASE_OUT_BACK
            ),
        )
        self.__searchIcon = IconButton(
            icon=icons.SEARCH_ROUNDED,
            icon_size=25,
            bgcolor="#1D7D81",
            icon_color=colors.WHITE,
            hover_color="#9cbab7",
            on_click=self.__showSearchBar
        )

        self.content = Row(
            controls=[
                self.__searchEntry,
                self.__searchIcon
            ]
        )

    def getSearchEntry(self):
        return self.__searchEntry.value

    def onChange(self, handler: Any):
        self.__searchEntry.on_change = handler

    flag = True

    def __showSearchBar(self, e):
        global flag
        if self.flag:
            self.border = border.only(bottom=BorderSide(width=2.5, color="#1D7D81"))
            self.__searchEntry.width = 300
            self.__searchIcon.icon = icons.CLEAR_ROUNDED
            self.__searchIcon.bgcolor = colors.TRANSPARENT
            self.flag = False
        else:
            # self.loadDataFunc()
            self.__searchEntry.value = ""
            self.__searchEntry.width = 0
            self.__searchIcon.icon = icons.SEARCH_ROUNDED
            self.__searchIcon.bgcolor = "#1D7D81"
            self.flag = True
            self.update()
            sleep(0.4)
            self.border = border.only(bottom=BorderSide(width=0, color=colors.TRANSPARENT))
        self.update()

# endregion
