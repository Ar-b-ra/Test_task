import json
from wsgiref.simple_server import make_server

from db.db_resources import ResourcesDataBaseManager
from logger import root_logger, init_logger_levels

test_db = "test_db"
data_base = ResourcesDataBaseManager(dbname=test_db, user="postgres", password="password", host="localhost", port=5432)


def application(environ, start_response):
    status = "200 OK"
    headers = [("Content-type", "text/plain; charset=utf-8")]
    start_response(status, headers)
    root_logger.info(headers)
    path = environ.get("PATH_INFO", "/")
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0
    request_method = environ["REQUEST_METHOD"]
    request_body = environ["wsgi.input"].read(request_body_size)
    root_logger.info(request_body.decode("UTF-8"))
    if path == "/resources":
        if request_method == "GET":
            return [str(data).encode("UTF-8") for data in data_base.get_resources()]
        elif request_method == "POST":
            prepared_json = json.loads(request_body)
            root_logger.info(prepared_json)
    elif environ["REQUEST_METHOD"] == "POST":
        if path == "/":
            return [b"Received POST request"]
    elif environ["REQUEST_METHOD"] == "PATCH":
        pass
    return [b"404 Not Found"]


if __name__ == "__main__":
    host = "localhost"
    port = 8000
    init_logger_levels()
    data_base.prepare_test_db()
    data_base.create_base_tables()
    with make_server(host, port, application) as httpd:
        root_logger.info(f"Сервер запущен на https://{host}:{port}...")
        httpd.serve_forever()
