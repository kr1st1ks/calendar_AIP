from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTimeEdit, QTextEdit, QPushButton, QMessageBox, QComboBox
)
from PyQt5.QtCore import QTime

class AddEventDialog(QDialog):  # Изменено с QWidget на QDialog
    def __init__(self, date, schedule_manager):
        super().__init__()
        self.date = date
        self.schedule_manager = schedule_manager
        self.setWindowTitle("Добавить событие")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        date_label = QLabel("Дата:")
        self.layout.addWidget(date_label)
        date_input = QLineEdit(self.date)
        self.layout.addWidget(date_input)

        start_time_label = QLabel("Время начала:")
        self.layout.addWidget(start_time_label)
        start_time_input = QTimeEdit()
        start_time_input.setTime(QTime(9, 0))
        self.layout.addWidget(start_time_input)

        end_time_label = QLabel("Время окончания:")
        self.layout.addWidget(end_time_label)
        end_time_input = QTimeEdit()
        end_time_input.setTime(QTime(10, 0))
        self.layout.addWidget(end_time_input)

        description_label = QLabel("Описание:")
        self.layout.addWidget(description_label)
        description_input = QTextEdit()
        self.layout.addWidget(description_input)

        theme_label = QLabel("Тема:")
        self.layout.addWidget(theme_label)
        theme_input = QComboBox()
        theme_input.setEditable(True)
        theme_input.addItem("")
        all_themes = set()
        for date, events in self.schedule_manager.get_schedule().items():
            for event in events:
                all_themes.add(event['theme'])
        for theme in sorted(all_themes):
            theme_input.addItem(theme)
        self.layout.addWidget(theme_input)

        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)
        add_button = QPushButton("Добавить")
        cancel_button = QPushButton("Отмена")
        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)

        def add_event():
            date = date_input.text()
            start_time = start_time_input.time().toString("HH:mm")
            end_time = end_time_input.time().toString("HH:mm")
            theme = theme_input.currentText().strip()
            description = description_input.toPlainText()

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

            self.schedule_manager.add_event(date, start_time, end_time, theme, description)
            QMessageBox.information(self, "Успех", "Событие добавлено!")
            self.close()

        add_button.clicked.connect(add_event)
        cancel_button.clicked.connect(self.close)