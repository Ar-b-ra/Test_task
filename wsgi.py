import argparse
import json
from wsgiref.simple_server import make_server

from db.db_resources import ResourcesDataBaseManager
from logger import root_logger, init_logger_levels


def application(environ, start_response):
    status = "200 OK"
    headers = [("Content-type", "text/plain; charset=utf-8")]
    start_response(status, headers)
    root_logger.info(headers)
    path = environ.get("PATH_INFO", "/")
    request_method = environ["REQUEST_METHOD"]

    answer = "404 Not Found"

    try:
        request_body_size = int(environ.get("CONTENT_LENGTH", 0))
        request_body = environ["wsgi.input"].read(request_body_size)
        root_logger.info(request_body.decode("UTF-8"))
        prepared_json = json.loads(request_body)
    except ValueError:
        prepared_json = {}

    if path == "/resources":

        if request_method == "POST":
            root_logger.info(prepared_json)
            answer = data_base.create_resource_type(
                resource_name=prepared_json["type"],
                max_speed=prepared_json["max_speed"],
            )

        elif request_method == "GET":
            answer = [
                str(json.dumps(data))
                for data in data_base.get_resource_types(
                    resource_type_name=prepared_json.get("type")
                )
            ] if prepared_json else [data_base.get_resource_types()]

        elif request_method == "UPDATE":
            answer = data_base.update_resource_type(resource_type=prepared_json["type"],
                                                    max_speed=prepared_json["max_speed"])

        elif request_method == "DELETE":
            if isinstance(prepared_json, list):
                for single_json in prepared_json:
                    answer = data_base.delete_resource_type(single_json['type'])
            else:
                answer = data_base.delete_resource_type(prepared_json['type'])


    elif path == "/resources/id":
        if request_method == "POST":
            answer = data_base.create_resource(resource_name=prepared_json["name"],
                                               resource_type=prepared_json["type"],
                                               current_speed=prepared_json["speed"])

        elif request_method == "DELETE":
            answer = data_base.delete_resource(resource_name=prepared_json['name'])

    return [json.dumps({"result": answer}).encode("UTF-8")]


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
    with make_server(host, port, application) as httpd:
        root_logger.info(f"Сервер запущен на https://{host}:{port}...")
        httpd.serve_forever()
