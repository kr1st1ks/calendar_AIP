import re
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTimeEdit, QTextEdit, QPushButton, QMessageBox, QComboBox
)
from PyQt5.QtCore import QTime, QDate


class AddEventDialog(QDialog):
    def __init__(self, date, schedule_manager):
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

        self.date = date
        self.schedule_manager = schedule_manager
        self.setWindowTitle("Добавить событие")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.date_input = QLineEdit(self.date)
        self.start_time_input = QTimeEdit()
        self.end_time_input = QTimeEdit()
        self.description_input = QTextEdit()
        self.theme_input = QComboBox()

        self._setup_ui()

    def _setup_ui(self):
        # Поле для даты
        date_label = QLabel("Дата:")
        self.layout.addWidget(date_label)
        self.layout.addWidget(self.date_input)

        # Поля для времени
        start_time_label = QLabel("Время начала:")
        self.layout.addWidget(start_time_label)
        self.start_time_input.setTime(QTime(9, 0))
        self.layout.addWidget(self.start_time_input)

        end_time_label = QLabel("Время окончания:")
        self.layout.addWidget(end_time_label)
        self.end_time_input.setTime(QTime(10, 0))
        self.layout.addWidget(self.end_time_input)

        # Поле для описания
        description_label = QLabel("Описание:")
        self.layout.addWidget(description_label)
        self.layout.addWidget(self.description_input)

        # Поле для выбора темы
        theme_label = QLabel("Тема:")
        self.layout.addWidget(theme_label)
        self.theme_input.setEditable(True)
        self.theme_input.addItem("")
        all_themes = set()
        for date, events in self.schedule_manager.get_schedule().items():
            for event in events:
                all_themes.add(event['theme'])
        for theme in sorted(all_themes):
            self.theme_input.addItem(theme)
        self.layout.addWidget(self.theme_input)

        # Кнопки
        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)
        add_button = QPushButton("Добавить")
        cancel_button = QPushButton("Отмена")
        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)

        add_button.clicked.connect(self._add_event)
        cancel_button.clicked.connect(self.close)

    def _add_event(self):
        date = self.date_input.text()
        start_time = self.start_time_input.time().toString("HH:mm")
        end_time = self.end_time_input.time().toString("HH:mm")
        theme = self.theme_input.currentText().strip()
        description = self.description_input.toPlainText().strip()

        # Проверка на пустую тему
        if not theme:
            QMessageBox.warning(self, "Ошибка", "Тема не может быть пустой!")
            return

        # Проверка на пустое описание
        if not description:
            QMessageBox.warning(self, "Ошибка", "Описание не может быть пустым!")
            return

        # Проверка: время начала должно быть раньше времени окончания
        if start_time >= end_time:
            QMessageBox.warning(self, "Ошибка", "Время начала должно быть раньше времени окончания!")
            return

        # Проверка на корректность формата даты (ГГГГ-ММ-ДД)
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            QMessageBox.warning(self, "Ошибка", "Неверный формат даты! Ожидаемый формат: ГГГГ-ММ-ДД.")
            return

        # Проверка на существование даты
        try:
            date_obj = QDate.fromString(date, "yyyy-MM-dd")
            if not date_obj.isValid():
                raise ValueError("Некорректная дата.")
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", f"Ошибка в дате: {str(e)}")
            return

        # Проверка на пересечения с другими событиями
        for event in self.schedule_manager.get_schedule(date):
            if not (end_time <= event['start_time'] or start_time >= event['end_time']):
                reply = QMessageBox.question(
                    self,
                    "Накладка",
                    f"Событие пересекается с '{event['description']}' "
                    f"({event['start_time']} - {event['end_time']}). Добавить всё равно?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return

        # Добавление события в расписание
        self.schedule_manager.add_event(date, start_time, end_time, theme, description)
        QMessageBox.information(self, "Успех", "Событие добавлено!")
        self.close()
