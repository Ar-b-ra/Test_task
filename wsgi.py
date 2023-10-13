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

    try:
        request_body_size = int(environ.get("CONTENT_LENGTH", 0))
        request_body = environ["wsgi.input"].read(request_body_size)
        root_logger.info(request_body.decode("UTF-8"))
        prepared_json = json.loads(request_body)
    except ValueError:
        prepared_json = {}

    if path == "/resources":
        if request_method == "GET":
            answer = [
                str(json.dumps(data)).encode("UTF-8")
                for data in data_base.get_resources(
                    resource_name=prepared_json.get("name")
                )
            ]

        elif request_method == "POST":
            root_logger.info(prepared_json)
            data_base.create_resource_type(
                resource_name=prepared_json["type"],
                max_speed=prepared_json["max_speed"],
            )
            answer = [b"Done!"]
        elif request_method == "DELETE":
            if isinstance(prepared_json, list):
                for single_json in prepared_json:
                    data_base.delete_rows(
                        table="resources", condition=f"'name'={single_json['name']}"
                    )
            else:
                data_base.delete_rows(
                    table="resources", condition=f"'name'={prepared_json['name']}"
                )
            answer = [f"All resources for {prepared_json} was deleted".encode("UTF-8")]
        else:
            answer = [b"What do you mean?"]
        return answer
    elif path == "/resources/id":
        pass
    return [b"404 Not Found"]


if __name__ == "__main__":
    host = "localhost"
    port = 8000
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
