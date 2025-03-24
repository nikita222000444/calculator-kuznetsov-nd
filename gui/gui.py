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

        self.result_label = QLabel("Результат: ", self)
        

        self.submit_button = QPushButton("Отправить", self)
        self.submit_button.clicked.connect(self.send_request)

        # Компоновка виджетов
        layout = QVBoxLayout()
        layout.addWidget(self.expression_input)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        
    def send_request(self):
        expression = self.expression_input.text()
        use_float = self.float_checkbox.isChecked()

        url = "http://localhost:8000/calc"
        

        try:
            # Отправляем POST-запрос на сервер
            response = requests.post(
                url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(expression)
            )

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
