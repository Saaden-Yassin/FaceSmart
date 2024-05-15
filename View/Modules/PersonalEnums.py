import math
import re
from enum import Enum
from flet import *


# region AppColors
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


# endregion

# region ProjectState
class ProjectState(Enum):
    TO_DO = 0
    START = 25
    IN_PROGRESS = 50
    TESTING = 75
    COMPLETED = 100


# endregion

# region PoppinsFont
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


# endregion

# region ValidateReg
class ValidateReg(Enum):
    USERNAME = (r"^\w+$", "Invalid username")
    EMAIL = (r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', "Email format must be xxxxx@exemple.xxx")
    PASSWORD = (r'\w{8,}', "Password must be at least 8 characters long and contain at least 1 letter and 1 digit")
    FIRST_LAST_NAME = (r'^[a-zA-Z]{2,}$', "First name must contain at least 2 letters")
    AGE = (r'^\d{1,100}$', "Age must be between 1 and 100")

    @classmethod
    def validate(cls, value, pattern):
        return re.match(pattern, value) is not None
# endregion
