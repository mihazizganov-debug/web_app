import http.server
import os
import socketserver
from urllib.parse import parse_qs, urlparse

PORT = 8080


class Handler(http.server.SimpleHTTPRequestHandler):
    """Обработчик HTTP-запросов."""

    def do_GET(self) -> None:
        """Обработка GET-запросов. Возвращает HTML-страницы."""

        parsed = urlparse(self.path)

        # Маршруты для HTML страниц
        routes = {
            "/": "templates/index.html",
            "/catalog": "templates/catalog.html",
            "/category": "templates/category.html",
            "/contacts": "templates/contacts.html",
        }

        # Обработка статических файлов (CSS, JS, картинки)
        if parsed.path.startswith("/static/"):
            file_path = parsed.path[1:]
            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    content = f.read()
                if file_path.endswith(".css"):
                    content_type = "text/css"
                elif file_path.endswith(".js"):
                    content_type = "application/javascript"
                elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
                    content_type = "image/jpeg"
                elif file_path.endswith(".png"):
                    content_type = "image/png"
                else:
                    content_type = "application/octet-stream"
                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404)
            return

        # Обработка HTML страниц
        if parsed.path in routes:
            try:
                with open(routes[parsed.path], "r", encoding="utf-8") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
            except FileNotFoundError:
                self.send_error(404)
        else:
            self.send_error(404)

    def do_POST(self) -> None:
        """Обработка POST-запросов (форма на странице Контакты)."""
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        parsed_data = parse_qs(post_data)

        print("=" * 50)
        print("📨 Получены данные из формы:")
        for key, value in parsed_data.items():
            print(f"  {key}: {value[0]}")
        print("=" * 50)

        response = """<!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Сообщение отправлено</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container text-center mt-5">
                <h1>✅ Спасибо за сообщение!</h1>
                <p>Мы ответим вам в ближайшее время.</p>
                <a href="/contacts" class="btn btn-primary">Вернуться к контактам</a>
            </div>
        </body>
        </html>"""

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(response.encode("utf-8"))


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🌐 Сервер на http://localhost:{PORT}")
        print("📂 Страницы:")
        print("   /         - Главная")
        print("   /catalog  - Каталог")
        print("   /category - Категория")
        print("   /contacts - Контакты")
        print("")
        print("💡 Отправь форму на странице /contacts — данные появятся в терминале")
        print("")
        httpd.serve_forever()
