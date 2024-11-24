from docx import Document
from docx.shared import Pt
from docx.enum.table import WD_ALIGN_VERTICAL

def export_schedule_to_docx(schedule, file_name):
    doc = Document()
    doc.add_heading("Расписание", 0)

    table = doc.add_table(rows=1, cols=5)
    headers = table.rows[0].cells
    headers[0].text = "Дата"
    headers[1].text = "Время начала"
    headers[2].text = "Время окончания"
    headers[3].text = "Тема"
    headers[4].text = "Описание"

    for cell in headers:
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].alignment = 1

    table.columns[0].width = Pt(80)
    table.columns[1].width = Pt(80)
    table.columns[2].width = Pt(80)
    table.columns[3].width = Pt(120)
    table.columns[4].width = Pt(20)

    for date, events in sorted(schedule.items()):
        for event in events:
            row_cells = table.add_row().cells
            row_cells[0].text = date
            row_cells[1].text = event['start_time']
            row_cells[2].text = event['end_time']
            row_cells[3].text = event['theme']
            row_cells[4].text = event['description']

            row_cells[0].paragraphs[0].alignment = 0
            row_cells[1].paragraphs[0].alignment = 0
            row_cells[2].paragraphs[0].alignment = 0
            row_cells[3].paragraphs[0].alignment = 0

            for paragraph in row_cells[4].paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)

            for cell in row_cells:
                cell.paragraphs[0].alignment = 3
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    doc.save(file_name)