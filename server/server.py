from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse
import subprocess

# Класс обработчика запросов
class CalculatorHandler(BaseHTTPRequestHandler):
    # Обработка POST-запросов
    def do_POST(self):
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
                except json.JSONDecodeError:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode('utf-8'))
                    return

                # Вычисляем выражение с помощью app.exe
                try:
                    result = self.evaluate_with_app_exe(expression, use_float)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(str(result)).encode('utf-8'))
                except subprocess.CalledProcessError as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": f"app.exe failed: {e.output.decode()}"}).encode('utf-8'))
                except FileNotFoundError:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "app.exe not found"}).encode('utf-8'))
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Internal server error"}).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode('utf-8'))

    # Метод для вычисления выражения с помощью app.exe
    def evaluate_with_app_exe(self, expression, use_float):
