from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse
import subprocess
import structlog
import sys

# Класс обработчика запросов
class CalculatorHandler(BaseHTTPRequestHandler):
    # Обработка POST-запросов
    def do_POST(self):
    
    # Метод для вычисления выражения с помощью app.exe
    def evaluate_with_app_exe(self, expression, use_float):
