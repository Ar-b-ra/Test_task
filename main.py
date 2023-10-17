import argparse
import json
from wsgiref.simple_server import make_server

from controllers.main_controller import Controller
from data_base_manager.resource_database_manager import ResourcesDataBaseManager
from logger import root_logger, init_logger_levels


def application(environ, start_response):
    headers = [("Content-type", "text/plain; charset=utf-8")]

    root_logger.info(headers)
    url_path = environ.get("PATH_INFO", "/")
    request_method = environ["REQUEST_METHOD"]

    try:
        request_body_size = int(environ.get("CONTENT_LENGTH", 0))
        request_body = environ["wsgi.input"].read(request_body_size)
        root_logger.info(request_body.decode("UTF-8"))
        prepared_json = json.loads(request_body)
    except ValueError:
        prepared_json = {}

    controller_callback = router.resolve(url=url_path, method=request_method)

    status, body = controller_callback(prepared_json)
    start_response(status, headers)
    return [json.dumps({"result": body}).encode("UTF-8")]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Добавляем опциональные аргументы для адреса хоста и порта
    parser.add_argument('--host', default='localhost', type=str, help='Адрес хоста')
    parser.add_argument('--port', '-p', default=8000, type=int, help='Порт')

    # Парсим аргументы командной строки
    args = parser.parse_args()

    # Выводим адрес хоста и порт
    root_logger.debug(f"Host = {args.host}, port = {args.port}")

    host = args.host
    port = args.port
    test_db = "test_db"
    data_base = ResourcesDataBaseManager(
        dbname=test_db,
        user="postgres",
        password="password",
        host="localhost",
        port=5432,
    )
    init_logger_levels()
    data_base.prepare_test_db()
    data_base.create_base_tables()
    data_base.create_fixtures()
    router = Controller(data_base=data_base)
    with make_server(host, port, application) as httpd:
        root_logger.info(f"Сервер запущен на https://{host}:{port}...")
        httpd.serve_forever()
