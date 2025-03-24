import sys
import json
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QCheckBox, QLabel
)


class CalculatorGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Настройка окна
        self.setWindowTitle("Калькулятор")
        self.setGeometry(100, 100, 400, 200)

        # Создание виджетов
        self.expression_input = QLineEdit(self)
        self.expression_input.setPlaceholderText("Введите выражение (например, 10 / 3)")
        
        # Валидатор: разрешаем только цифры, операторы и пробелы
        validator = QRegularExpressionValidator(
            QRegularExpression(r'^[0-9+\-*/\s]+$'),  # Регулярное выражение
            self.expression_input
        )
        self.expression_input.setValidator(validator)

        self.result_label = QLabel("Результат: ", self)
        
        self.float_checkbox = QCheckBox("Использовать числа с плавающей точкой (--float)", self)

        self.submit_button = QPushButton("Отправить", self)
        self.submit_button.clicked.connect(self.send_request)

        # Компоновка виджетов
        layout = QVBoxLayout()
        layout.addWidget(self.expression_input)
        layout.addWidget(self.float_checkbox)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def send_request(self):
        expression = self.expression_input.text()
        use_float = self.float_checkbox.isChecked()

        # Формируем URL с параметром float
        url = "http://localhost:8000/calc"
        if use_float:
            url += "?float=true"

        try:
            # Отправляем POST-запрос на сервер
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(expression)
            )

            # Проверяем статус ответа
            if response.status_code == 200:
                # Отображаем результат
                self.result_label.setText(f"Результат: {response.text}")
            else:
                # Отображаем ошибку
                self.result_label.setText(f"Ошибка: {response.text}")

        except requests.exceptions.RequestException as e:
            # Обрабатываем ошибки подключения
            self.result_label.setText(f"Ошибка подключения: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создаем и показываем окно
    window = CalculatorGUI()
    window.show()

    # Запускаем цикл обработки событий
    sys.exit(app.exec())
