from http.server import HTTPServer

from logger import root_logger
from request_handler import HTTPRequestHandler

if __name__ == "__main__":
    host = "localhost"
    port = 8000

    server = HTTPServer((host, port), HTTPRequestHandler)
    root_logger.info(f"Сервер запущен на http://{host}:{port}...")

    server.serve_forever()
