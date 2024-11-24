from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTimeEdit, QTextEdit, QPushButton, QMessageBox, QComboBox
)
from PyQt5.QtCore import QTime

class EditEventDialog(QDialog):  # Изменено с QWidget на QDialog
    def __init__(self, date, start_time, end_time, theme, description, schedule_manager):
        super().__init__()
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.theme = theme
        self.description = description
        self.schedule_manager = schedule_manager
        self.setWindowTitle("Редактировать событие")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        start_time_label = QLabel("Время начала:")
        self.layout.addWidget(start_time_label)
        start_time_input = QTimeEdit(QTime.fromString(start_time, "HH:mm"))
        self.layout.addWidget(start_time_input)

        end_time_label = QLabel("Время окончания:")
        self.layout.addWidget(end_time_label)
        end_time_input = QTimeEdit(QTime.fromString(end_time, "HH:mm"))
        self.layout.addWidget(end_time_input)

        description_label = QLabel("Описание:")
        self.layout.addWidget(description_label)
        description_input = QTextEdit(description)
        self.layout.addWidget(description_input)

        theme_label = QLabel("Тема:")
        self.layout.addWidget(theme_label)
        theme_input = QComboBox()
        theme_input.setEditable(True)
        theme_input.addItem("Выберите или введите тему...")
        all_themes = set()
        for date, events in self.schedule_manager.get_schedule().items():
            for event in events:
                all_themes.add(event['theme'])
        for theme in sorted(all_themes):
            theme_input.addItem(theme)
        theme_input.setCurrentText(theme)
        self.layout.addWidget(theme_input)

        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)
        save_button = QPushButton("Сохранить")
        cancel_button = QPushButton("Отмена")
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        def save_changes():
            new_start_time = start_time_input.time().toString("HH:mm")
            new_end_time = end_time_input.time().toString("HH:mm")
            new_description = description_input.toPlainText()
            new_theme = theme_input.currentText().strip()

            for event in self.schedule_manager.get_schedule(self.date):
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

            self.schedule_manager.edit_event(self.date, self.start_time, self.end_time, self.theme, self.description,
                                             new_start_time, new_end_time, new_theme, new_description)
            QMessageBox.information(self, "Успех", "Событие успешно обновлено.")
            self.close()

        save_button.clicked.connect(save_changes)
        cancel_button.clicked.connect(self.close)