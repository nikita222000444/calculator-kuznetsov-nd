from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse
import subprocess
import structlog
import sys

# Настройка structlog
def configure_logging():

    # Логгер для записи в файл
    file_logger = structlog.PrintLogger(file=open("server/logs.log", "a"))

    # Функция для записи логов в файл с отступами
    def file_logger_with_indent(logger, method_name, event_dict):
        # Форматируем JSON с отступами
        formatted_log = json.dumps(event_dict, indent=2)
        # Записываем в файл
        file_logger.msg(formatted_log)
        return event_dict

    # Настройка structlog
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            file_logger_with_indent,  # Записываем в файл с отступами
            structlog.processors.JSONRenderer(indent=2, sort_keys=True),  # Для консоли
        ],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),  # Используем PrintLogger
        wrapper_class=structlog.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Возвращаем логгер
    return structlog.get_logger()

# Создаем логгер
logger = configure_logging()

# Класс обработчика запросов
class CalculatorHandler(BaseHTTPRequestHandler):
    # Обработка POST-запросов
    def do_POST(self):
        # Логируем поступивший запрос
        logger.info(
            "Request received",
            path=self.path,
            method=self.command,
            headers=dict(self.headers),
        )

        # Проверяем путь запроса
        if self.path.startswith('/calc'):
            try:
                # Парсим query-параметры
                query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                use_float = query_params.get('float', ['false'])[0].lower() == 'true'

                # Читаем тело запроса
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)

                # Парсим JSON
                try:
                    expression = json.loads(post_data.decode('utf-8'))
                    logger.info("Expression parsed", expression=expression)
                except json.JSONDecodeError:
                    logger.error("Invalid JSON received")
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode('utf-8'))
                    return

                # Вычисляем выражение с помощью app.exe
                try:
                    result = self.evaluate_with_app_exe(expression, use_float)
                    logger.info(
                        "Expression evaluated",
                        expression=expression,
                        result=result,
                        use_float=use_float,
                    )
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(str(result)).encode('utf-8'))
                except subprocess.CalledProcessError as e:
                    logger.error(
                        "app.exe failed",
                        expression=expression,
                        error=e.output.decode(),
                        use_float=use_float,
                    )
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": f"app.exe failed: {e.output.decode()}"}).encode('utf-8'))
                except Exception as e:
                    logger.error("Unexpected error", error=str(e))
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            except Exception as e:
                logger.error("Internal server error", error=str(e))
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Internal server error"}).encode('utf-8'))
        else:
            logger.warning("Path not found", path=self.path)
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode('utf-8'))

    # Метод для вычисления выражения с помощью app.exe
    def evaluate_with_app_exe(self, expression, use_float):
        # Подготавливаем входные данные для app.exe
        input_data = f"{expression}\n"

        # Аргументы для app.exe
        args = ['build/app.exe']
        if use_float:
            args.append('--float')

        # Вызываем app.exe
        process = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=input_data)

        # Проверяем код завершения
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, 'app.exe', stderr)

        # Возвращаем результат
        return stdout.strip()

# Запуск сервера
def run(server_class=HTTPServer, handler_class=CalculatorHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logger.info("Starting server", address=server_address, port=port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Stopping server")
        httpd.server_close()

if __name__ == "__main__":
    run()
