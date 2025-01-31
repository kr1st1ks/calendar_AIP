from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QCalendarWidget, QTableWidget, QTableWidgetItem, QPushButton, QComboBox
)
from PyQt5.QtCore import QDate

class ViewScheduleDialog(QDialog):  # Изменено с QWidget на QDialog
    def __init__(self, schedule_manager):
        super().__init__()
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5FFFA; /* Светлый оттенок зелени для заднего фона */
            }

            QPushButton {
                background-color: #6B8E23; /* Мшистый зеленый */
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #228B22; /* Темно-зеленый при наведении */
            }

            QPushButton:pressed {
                background-color: #8B4513; /* Землистый коричневый при нажатии */
            }

            QCalendarWidget {
                background-color: #F0FFF0; /* Очень светло-зеленый */
                border: 1px solid #6B8E23;
                font-size: 14px;
                color: #2E8B57; /* Темно-зеленый для текста */
            }

            QCalendarWidget QAbstractItemView {
                selection-background-color: #90EE90; /* Светло-зеленый для выделения */
                gridline-color: #6B8E23;
                border: 1px solid #6B8E23;
            }

            QCalendarWidget QToolButton {
                background-color: #228B22; /* Темно-зеленый */
                color: white;
                font-weight: bold;
                border: none;
                padding: 10px;
            }

            QCalendarWidget QToolButton:hover {
                background-color: #6B8E23; /* Мшистый зеленый */
            }

            QCalendarWidget QToolButton:pressed {
                background-color: #8B4513; /* Землистый коричневый */
            }

            QCalendarWidget QHeaderView::section {
                background-color: #6B8E23; /* Мшистый зеленый */
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                text-align: center;
            }

            QCalendarWidget QTextCharFormat {
                color: #2E8B57;
            }

            QTableWidget {
                border: 1px solid #8B4513;
                font-size: 14px;
                background-color: #F0FFF0;
                gridline-color: #6B8E23;
            }

            QTableWidget::item {
                padding: 10px;
            }

            QTableWidget::item:hover {
                background-color: #90EE90;
            }

            QHeaderView::section {
                background-color: #6B8E23;
                color: white;
                font-size: 16px;
                padding: 10px;
            }

            QLineEdit {
                border: 1px solid #6B8E23;
                border-radius: 5px;
                padding: 8px;
                background-color: #FFFFFF;
                color: #2E8B57;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 2px solid #228B22;
            }

            QMessageBox {
                background-color: #F5FFFA;
                color: #2E8B57;
                font-size: 14px;
            }

            QFileDialog {
                background-color: #F5FFFA;
                color: #2E8B57;
                font-size: 14px;
            }
        """)

        self.schedule_manager = schedule_manager
        self.setWindowTitle("Просмотреть расписание")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        filter_layout = QHBoxLayout()
        self.layout.addLayout(filter_layout)

        start_date_label = QLabel("Выберите дату начала:")
        filter_layout.addWidget(start_date_label)
        start_date_input = QCalendarWidget()
        start_date_input.setSelectedDate(QDate.currentDate())
        filter_layout.addWidget(start_date_input)

        range_label = QLabel("Выберите диапазон:")
        filter_layout.addWidget(range_label)
        date_range_input = QComboBox()
        date_range_input.addItem("1 неделя")
        date_range_input.addItem("1 месяц")
        date_range_input.addItem("3 месяца")
        filter_layout.addWidget(date_range_input)

        theme_filter_label = QLabel("Фильтр по теме:")
        filter_layout.addWidget(theme_filter_label)
        theme_filter_input = QComboBox()
        theme_filter_input.addItem("Все темы")
        all_themes = set()
        for date, events in self.schedule_manager.get_schedule().items():
            for event in events:
                all_themes.add(event['theme'])
        for theme in sorted(all_themes):
            theme_filter_input.addItem(theme)
        filter_layout.addWidget(theme_filter_input)

        filter_button = QPushButton("Применить фильтр")
        filter_layout.addWidget(filter_button)

        schedule_table = QTableWidget()
        schedule_table.setColumnCount(5)
        schedule_table.setHorizontalHeaderLabels(["Дата", "Время начала", "Время окончания", "Тема", "Описание"])
        self.layout.addWidget(schedule_table)

        def populate_table(filtered_schedule=None):
            schedule_table.setRowCount(0)
            data = self.schedule_manager.get_schedule().items() if filtered_schedule is None else filtered_schedule.items()
            selected_start_date = start_date_input.selectedDate()
            selected_range = date_range_input.currentText()
            if selected_range == "1 неделя":
                end_date = selected_start_date.addDays(7)
            elif selected_range == "1 месяц":
                end_date = selected_start_date.addMonths(1)
            elif selected_range == "3 месяца":
                end_date = selected_start_date.addMonths(3)
            selected_theme = theme_filter_input.currentText()
            for date, events in sorted(data):
                row_date = QDate.fromString(date, "yyyy-MM-dd")
                if selected_start_date <= row_date <= end_date:
                    for event in sorted(events, key=lambda e: e['start_time']):
                        if selected_theme == "Все темы" or event['theme'] == selected_theme:
                            row = schedule_table.rowCount()
                            schedule_table.insertRow(row)
                            schedule_table.setItem(row, 0, QTableWidgetItem(date))
                            schedule_table.setItem(row, 1, QTableWidgetItem(event['start_time']))
                            schedule_table.setItem(row, 2, QTableWidgetItem(event['end_time']))
                            schedule_table.setItem(row, 3, QTableWidgetItem(event['theme']))
                            schedule_table.setItem(row, 4, QTableWidgetItem(event['description']))

        def apply_filter():
            filtered_schedule = {}
            selected_start_date = start_date_input.selectedDate().toString("yyyy-MM-dd")
            selected_range = date_range_input.currentText()
            if selected_range == "1 неделя":
                end_date = start_date_input.selectedDate().addDays(7)
            elif selected_range == "1 месяц":
                end_date = start_date_input.selectedDate().addMonths(1)
            elif selected_range == "3 месяца":
                end_date = start_date_input.selectedDate().addMonths(3)
            for date, events in self.schedule_manager.get_schedule().items():
                row_date = QDate.fromString(date, "yyyy-MM-dd")
                if start_date_input.selectedDate() <= row_date <= end_date:
                    filtered_schedule[date] = events
            populate_table(filtered_schedule)

        filter_button.clicked.connect(apply_filter)
        populate_table()

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)
        self.layout.addWidget(close_button)