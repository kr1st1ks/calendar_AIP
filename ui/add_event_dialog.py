import re

from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTimeEdit,
    QTextEdit, QPushButton, QMessageBox, QComboBox, QStyle, QStyledItemDelegate, QColorDialog
)
from PyQt5.QtCore import QTime, QDate, Qt, QRectF


class ColorDelegate(QStyledItemDelegate):
    """ Кастомный делегат для изменения цвета фона каждого элемента в QComboBox """

    def paint(self, painter, option, index):
        # Получаем цвет элемента (мы его сохранили в UserRole)
        color = index.data(Qt.UserRole)
        base_color = QColor(color)

        # Проверяем, наведен ли курсор
        if option.state & QStyle.State_MouseOver:
            fill_color = base_color.darker(120)  # Затемняем цвет при наведении
        else:
            fill_color = base_color

        # Создаем скругленный прямоугольник
        rect = QRectF(option.rect).adjusted(1, 2, -1, -1)  # Добавляем отступы
        radius = 6  # Радиус скругления

        # Рисуем фон с закругленными краями
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(fill_color))
        painter.setPen(QPen(Qt.NoPen))  # Без границ
        painter.drawRoundedRect(rect, radius, radius)

        # Рисуем стандартный текст
        painter.setPen(Qt.black)
        text_rect = option.rect.adjusted(6, 0, 0, 0)
        painter.drawText(text_rect, Qt.AlignVCenter | Qt.TextSingleLine, index.data())

class CustomComboBox(QComboBox):
    """ Кастомный QComboBox, который поддерживает изменение цвета элементов """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentIndexChanged.connect(self.updateColor)  # Обновляем стиль при смене элемента

    def addColoredItem(self, text, color):
        """ Добавляет элемент с цветом """
        self.addItem(text)
        index = self.count() - 1  # Индекс последнего элемента
        self.setItemData(index, color, Qt.UserRole)  # Сохраняем цвет в UserRole

        if index == 0:  # Если это первый элемент, сразу обновляем цвет
            self.updateColor(0)

    def updateColor(self, index):
        """ Обновляет цвет главной кнопки через CSS """
        color = self.itemData(index, Qt.UserRole)
        if color:
            base_color = QColor(color)

            self.setStyleSheet(f"""
            QComboBox {{
                background-color: {color};
                padding: 8px; 
                border-radius: 5px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: rgb(230, 224, 200);
                padding: 8px; 
                border-radius: 5px;
            }}
            QComboBox QAbstractItemView::item {{
                padding: 8px; 
            }}
            """)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        # Рисуем кастомную иконку стрелки прямо
        arrow = '▼'
        # Метрики шрифта
        fm = painter.fontMetrics()
        aw = fm.horizontalAdvance(arrow)
        ah = fm.height()

        # Позиционируем: справа с отступом, по центру по вертикали
        margin = 10
        x = self.width() - aw - margin
        # y — это базовая линия текста, поэтому подгоняем:
        y = (self.height() + fm.ascent() - fm.descent()) // 2

        painter.drawText(x, y, arrow)


class AddEventDialog(QDialog):
    def __init__(self, date, schedule_manager):
        super().__init__()
        self.color = QColor('#3e5d07')
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
        self.schedule_manager = schedule_manager
        self.setWindowTitle("Добавить событие")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.date_input = QLineEdit(self.date)
        self.start_time_input = QTimeEdit()
        self.end_time_input = QTimeEdit()
        self.description_input = QTextEdit()
        self.theme_input = CustomComboBox()
        self.theme_input.setItemDelegate(ColorDelegate())

        self._setup_ui()

    def _setup_ui(self):
        # Поле для даты
        date_label = QLabel("Дата:")
        self.layout.addWidget(date_label)
        self.date_input.setReadOnly(True)
        self.layout.addWidget(self.date_input)

        # Поля для времени
        time_layout = QHBoxLayout()

        start_time_group = QVBoxLayout()
        start_time_label = QLabel("Время начала:")
        start_time_group.addWidget(start_time_label)
        self.start_time_input.setTime(QTime(9, 0))
        start_time_group.addWidget(self.start_time_input)
        time_layout.addLayout(start_time_group)

        end_time_group = QVBoxLayout()
        end_time_label = QLabel("Время окончания:")
        end_time_group.addWidget(end_time_label)
        self.end_time_input.setTime(QTime(10, 0))
        end_time_group.addWidget(self.end_time_input)
        time_layout.addLayout(end_time_group)

        self.layout.addLayout(time_layout)

        # Поле для выбора темы
        theme_label = QLabel("Тема:")
        self.layout.addWidget(theme_label)
        self.theme_input.setEditable(True)
        self.theme_input.addColoredItem("", "white")
        all_themes = set()
        for date, events in self.schedule_manager.get_schedule().items():
            for event in events:
                all_themes.add(event['theme'])
        palette = ["#FFFFFF"]

        for i, theme in enumerate(sorted(all_themes)):
            color = palette[i % len(palette)]
            self.theme_input.addColoredItem(theme, color)

        self.layout.addWidget(self.theme_input)

        self.color_button = QPushButton("Цвет темы", self)
        self.layout.addWidget(self.color_button)
        self.color_button.clicked.connect(self.open_color_dialog)

        # Поле для описания
        description_label = QLabel("Описание:")
        self.layout.addWidget(description_label)
        self.description_input.setPlaceholderText("Введите описание события...")
        self.layout.addWidget(self.description_input)

        # Кнопки
        button_layout = QHBoxLayout()
        self.layout.addLayout(button_layout)

        add_button = QPushButton("Добавить")
        add_button.setStyleSheet("""
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

        button_layout.addWidget(add_button)
        button_layout.addWidget(cancel_button)

        add_button.clicked.connect(self._add_event)
        cancel_button.clicked.connect(self.close)

    def _add_event(self):
        date = self.date_input.text()
        start_time = self.start_time_input.time().toString("HH:mm")
        end_time = self.end_time_input.time().toString("HH:mm")
        theme = self.theme_input.currentText().strip()
        color = self.color.name()
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
        self.schedule_manager.add_event(date, start_time, end_time, theme, color, description)
        QMessageBox.information(self, "Успех", "Событие добавлено!")
        self.close()

    def open_color_dialog(self):
        # Открываем диалог выбора цвета
        self.color = QColorDialog.getColor(initial=QColor(255, 255, 255), parent=self,
                                      title="Выберите цвет")
        hover_color = self.color.darker(120)
        # Если пользователь не нажал Отмена
        if self.color.isValid():
            # Устанавливаем стиль кнопки: background-color
            self.color_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.color.name()};
                }}
                QPushButton:hover {{
                    background-color: {hover_color.name()};
                }}
            """)