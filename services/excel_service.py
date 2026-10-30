from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

from services.activity_service import ActivityService


class ExcelService:

    @staticmethod
    def export_activities(db, file_path: str):

        activities = ActivityService.get_all_activities(db)

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Activities"

        headers = [
            "ID",
            "Activity Name",
            "Duration (Minutes)",
            "Achievement",
            "Tags",
            "Created At"
        ]

        sheet.append(headers)

        for cell in sheet[1]:
            cell.font = Font(
                bold=True,
                color="FFFFFF"
            )

            cell.fill = PatternFill(
                start_color="263449",
                end_color="263449",
                fill_type="solid"
            )

            cell.alignment = Alignment(
                horizontal="center"
            )

        for activity in activities:

            tag_names = ", ".join(
                tag.name for tag in activity.tags
            )

            sheet.append([
                activity.id,
                activity.name,
                activity.duration_minutes,
                activity.achievement or "",
                tag_names,
                activity.created_at.strftime("%Y-%m-%d %H:%M")
            ])

        column_widths = [10, 30, 22, 40, 30, 22]

        for index, width in enumerate(column_widths, start=1):
            sheet.column_dimensions[
                get_column_letter(index)
            ].width = width

        sheet.freeze_panes = "A2"
        sheet.auto_filter.ref = sheet.dimensions

        workbook.save(file_path)

        return file_path