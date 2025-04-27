from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTimeEdit,
    QTextEdit, QPushButton, QMessageBox, QComboBox
)
from PyQt5.QtCore import QTime, QDate


class EditEventDialog(QDialog):
    def __init__(self, date, start_time, end_time, theme, description, schedule_manager):
        super().__init__()
        self.setStyleSheet("""
            QDialog {
                background-color: rgb(230, 224, 200);
                font-size: 14px;
            }

            QLabel {
                color: rgb(62, 93, 7);
                font-weight: bold;
            }

            QPushButton {
                background-color: rgb(62, 93, 7); 
                color: white; 
                font-size: 14px; 
                padding: 10px; 
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: rgb(62, 84, 7);
            }

            QPushButton:pressed {
                background-color: rgb(139, 93, 36);
            }

            QLineEdit, QTextEdit, QComboBox, QTimeEdit {
                background-color: white;
                border: 1px solid rgb(139, 93, 36);
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }

            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QTimeEdit:focus {
                border: 2px solid rgb(62, 93, 7);
            }

            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: rgb(230, 224, 200);
                border: 1px solid rgb(139, 93, 36);
            }

            QMessageBox {
                background-color: rgb(230, 224, 200);
            }

            QMessageBox QLabel {
                color: black;
                font-weight: normal;
            }

            QMessageBox QPushButton {
                min-width: 80px;
            }
        """)

        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.theme = theme
        self.description = description
        self.schedule_manager = schedule_manager
        self.setWindowTitle("Редактировать событие")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Поле для даты
        date_label = QLabel("Дата:")
        self.layout.addWidget(date_label)
        self.date_input = QLineEdit(self.date)
        self.date_input.setReadOnly(True)
        self.layout.addWidget(self.date_input)

        # Поля для времени
        time_layout = QHBoxLayout()

        start_time_group = QVBoxLayout()
        start_time_label = QLabel("Время начала:")
        start_time_group.addWidget(start_time_label)
        self.start_time_input = QTimeEdit(QTime.fromString(start_time, "HH:mm"))
        start_time_group.addWidget(self.start_time_input)
        time_layout.addLayout(start_time_group)

        end_time_group = QVBoxLayout()
        end_time_label = QLabel("Время окончания:")
        end_time_group.addWidget(end_time_label)
        self.end_time_input = QTimeEdit(QTime.fromString(end_time, "HH:mm"))
        end_time_group.addWidget(self.end_time_input)
        time_layout.addLayout(end_time_group)

        self.layout.addLayout(time_layout)

        # Поле для выбора темы
        theme_label = QLabel("Тема:")
        self.layout.addWidget(theme_label)
        self.theme_input = QComboBox()
        self.theme_input.setEditable(True)
        self.theme_input.addItem("")
        all_themes = set()
        for date, events in self.schedule_manager.get_schedule().items():
            for event in events:
                all_themes.add(event['theme'])
        for theme in sorted(all_themes):
            self.theme_input.addItem(theme)
        self.theme_input.setCurrentText(self.theme)
        self.layout.addWidget(self.theme_input)

        # Поле для описания
        description_label = QLabel("Описание:")
        self.layout.addWidget(description_label)
        self.description_input = QTextEdit(self.description)
        self.description_input.setPlaceholderText("Введите описание события...")
        self.layout.addWidget(self.description_input)

        # Кнопки
        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)

        save_button = QPushButton("Сохранить")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(62, 93, 7);
            }
            QPushButton:hover {
                background-color: rgb(62, 84, 7);
            }
        """)

        cancel_button = QPushButton("Отмена")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(139, 93, 36);
            }
            QPushButton:hover {
                background-color: rgb(122, 80, 28);
            }
        """)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        save_button.clicked.connect(self._save_changes)
        cancel_button.clicked.connect(self.close)

    def _save_changes(self):
        new_start_time = self.start_time_input.time().toString("HH:mm")
        new_end_time = self.end_time_input.time().toString("HH:mm")
        new_description = self.description_input.toPlainText().strip()
        new_theme = self.theme_input.currentText().strip()

        # Проверка на пустую тему
        if not new_theme:
            QMessageBox.warning(self, "Ошибка", "Тема не может быть пустой!")
            return

        # Проверка на пустое описание
        if not new_description:
            QMessageBox.warning(self, "Ошибка", "Описание не может быть пустым!")
            return

        # Проверка: время начала должно быть раньше времени окончания
        if new_start_time >= new_end_time:
            QMessageBox.warning(self, "Ошибка", "Время начала должно быть раньше времени окончания!")
            return

        # Проверка на пересечения с другими событиями
        for event in self.schedule_manager.get_schedule(self.date):
            if event['start_time'] != self.start_time or event['end_time'] != self.end_time or event['theme'] != self.theme or event['description'] != self.description:
                if not (new_end_time <= event['start_time'] or new_start_time >= event['end_time']):
                    reply = QMessageBox.question(
                        self,
                        "Накладка",
                        f"Событие пересекается с '{event['description']}' "
                        f"({event['start_time']} - {event['end_time']}). Сохранить изменения?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if reply == QMessageBox.No:
                        return

        self.schedule_manager.edit_event(
            self.date, self.start_time, self.end_time, self.theme, self.description,
            new_start_time, new_end_time, new_theme, new_description
        )
        QMessageBox.information(self, "Успех", "Событие успешно обновлено.")
        self.close()