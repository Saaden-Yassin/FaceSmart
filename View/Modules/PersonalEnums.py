import math
from enum import Enum
from flet import *


class AppColors(Enum):
    BLACK_GREEN_LINEAR_GRADIAN = LinearGradient(
        begin=alignment.top_right,
        end=alignment.bottom_left,
        colors=[
            "#173839",
            "#0D1F1F",
            "#173839",
            "#020402",
        ],
        tile_mode=GradientTileMode.REPEATED,
        rotation=math.pi / 3,
    )


class ProjectState(Enum):
    TO_DO = 0
    START = 25
    IN_PROGRESS = 50
    TESTING = 75
    COMPLETED = 100


class PoppinsFont(Enum):
    BLACK = "../assets/fonts/Poppins/Poppins-Black.ttf"
    BLACK_ITALIC = "../assets/fonts/Poppins/Poppins-BlackItalic.ttf"
    BOLD = "../assets/fonts/Poppins/Poppins-Bold.ttf"

    BOLD_ITALIC = "../assets/fonts/Poppins/Poppins-BoldItalic.ttf"
    EXTRA_BOLD = "../assets/fonts/Poppins/Poppins-ExtraBold.ttf"
    EXTRA_BOLD_ITALIC = "../assets/fonts/Poppins/Poppins-ExtraBoldItalic.ttf"
    EXTRA_LIGHT = "../assets/fonts/Poppins/Poppins-ExtraLight.ttf"
    EXTRA_LIGHT_ITALIC = "../assets/fonts/Poppins/Poppins-ExtraLightItalic.ttf"
    ITALIC = "../assets/fonts/Poppins/Poppins-Italic.ttf"
    LIGHT_ITALIC = "../assets/fonts/Poppins/Poppins-LightItalic.ttf"
    MEDIUM = "../assets/fonts/Poppins/Poppins-Medium.ttf"
    MEDIUM_ITALIC = "../assets/fonts/Poppins/Poppins-MediumItalic.ttf"
    REGULAR = "../assets/fonts/Poppins/Poppins-Regular.ttf"
    SEMI_BOLD = "../assets/fonts/Poppins/Poppins-SemiBold.ttf"
    SEMI_BOLD_ITALIC = "../assets/fonts/Poppins/Poppins-SemiBoldItalic.ttf"
    THIN = "../assets/fonts/Poppins/Poppins-Thin.ttf"
    THIN_ITALIC = "../assets/fonts/Poppins/Poppins-ThinItalic.ttf"
