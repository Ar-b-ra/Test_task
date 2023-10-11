from wsgiref.simple_server import make_server

from logger import root_logger


def application(environ, start_response):
    status = "200 OK"
    headers = [("Content-type", "text/plain; charset=utf-8")]

    start_response(status, headers)
    root_logger.info(headers)

    return [b"Hello world, asdsad"]


if __name__ == "__main__":
    with make_server("", 8000, application) as httpd:
        root_logger.info("Сервер запущен на порту 8000...")
        httpd.serve_forever()
