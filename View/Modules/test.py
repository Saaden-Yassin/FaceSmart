from flet import *

from datetime import *

def main(page: Page):
    def change_date(e):
        print(f"Date picker changed, value is {date_picker.value}")

    def date_picker_dismissed(e):
        print(f"Date picker dismissed, value is {date_picker.value}")

    date_picker = DatePicker(
        on_change=change_date,
        on_dismiss=date_picker_dismissed,
        current_date=datetime.now(),
    )

    page.overlay.append(date_picker)

    date_button = ElevatedButton(
        "Pick date",
        icon=icons.CALENDAR_MONTH,
        on_click=lambda _: date_picker.pick_date(),
    )

    page.add(date_button)


app(target=main, assets_dir="../assets")
