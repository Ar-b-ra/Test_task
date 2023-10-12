from http.server import HTTPServer

from db.db_resources import ResourcesDataBaseManager
from logger import init_logger_levels
from handlers.request_handler import HTTPRequestHandler

if __name__ == "__main__":
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
    host = "localhost"
    port = 8000
    HTTPRequestHandler.db = data_base
    server = HTTPServer((host, port), HTTPRequestHandler)
    server.serve_forever()
