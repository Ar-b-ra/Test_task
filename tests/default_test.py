import unittest
from db.data_base import DatabaseConnection

user = "postgres"
password = "password"
database_name = "test_db"
host = "localhost"


class SimpleHTTPRequestHandlerTests(unittest.TestCase):
    def setUp(self):
        self.connection = DatabaseConnection(user, password, host, 5432, database_name)
        self.connection.connect()

    def tearDown(self):
        self.connection.execute_query("DROP TABLE temp_table")
        self.connection.close()

    def test_connect_success(self):
        assert self.connection.connect()

    def test_connect_failure(self):
        connection = DatabaseConnection(
            user, "wrong_password", host, 5432, database_name
        )
        assert not connection.connect()

    # def test_create_table_existing_table(self):
    #     with self.assertLogs(level="WARNING") as log_capture:
    #         self.connection.create_table("existing_table")
    #         # Проверяем, что предупреждение было выдано
    #         assert (
    #             "Database with table_name = 'existing_table' already exists!"
    #             in log_capture.output
    #         )
    #
    # def test_create_table_new_table(self):
    #     with self.assertLogs(level="INFO") as log_capture:
    #         self.connection.create_table("new_table")
    #         # Проверяем, что таблица была создана успешно
    #         assert "Query executed successfully!" in log_capture.output
    #
    # def test_create_database(self):
    #     with self.assertLogs(level="INFO") as log_capture:
    #         self.connection.create_database("new_db")
    #         # Проверяем, что база данных была создана успешно
    #         assert "Query executed successfully!" in log_capture.output

    def test_delete_rows(self):
        # Создаем временную таблицу для теста
        self.connection.execute_query("DROP TABLE temp_table")
        self.connection.create_table(
            "temp_table", "id", foreign_key=None, table_params={"name": "VARCHAR(15)"}
        )
        self.connection.execute_query(
            "INSERT INTO temp_table (id, name) VALUES (1, 'John')"
        )
        self.connection.execute_query(
            "INSERT INTO temp_table (id, name) VALUES (2, 'Jane')"
        )
        self.connection.delete_rows("temp_table", "id=1")
        # Проверяем, что строка была успешно удалена
        self.connection.execute_query("SELECT * FROM temp_table")
        result = self.connection.cursor.fetchall()
        assert len(result) == 1

    # def test_execute_query_success(self):
    #     with self.assertLogs(level="INFO") as log_capture:
    #         self.connection.execute_query("SELECT * FROM existing_table")
    #         # Проверяем, что запрос был выполнен успешно
    #         assert "Query executed successfully!" in log_capture.output
    #
    # def test_execute_query_failure(self):
    #     with self.assertLogs(level="ERROR") as log_capture:
    #         self.connection.execute_query("SELECT * FROM non_existing_table")
    #         # Проверяем, что ошибка была выдана
    #         assert "Error while executing query" in log_capture.output


if __name__ == "__main__":
    unittest.main()
