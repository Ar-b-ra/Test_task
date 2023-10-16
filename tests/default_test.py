import unittest
from db.data_base import DatabaseConnection
from db.db_resources import ResourcesDataBaseManager

user = "postgres"
password = "password"
database_name = "test_db"
host = "localhost"

TIPPER = "tipper"
EXCAVATOR = "excavator"


class SimpleHTTPRequestHandlerTests(unittest.TestCase):
    def setUp(self):
        self.connection = ResourcesDataBaseManager(user, password, host, 5432, database_name)
        self.connection.connect()
        self.connection.create_base_tables()
        for name, max_speed in [(EXCAVATOR, 40), (TIPPER, 80)]:
            self.connection.create_resource_type(resource_name=name, max_speed=max_speed)
        for res_type, name, cur_speed in [(TIPPER, "101", 63), (TIPPER, "102", 85),
                                          (EXCAVATOR, "E103", 60), (EXCAVATOR, "E104", 104)]:
            self.connection.create_resource(resource_type=res_type, resource_name=name, current_speed=cur_speed)

    def tearDown(self):

        self.connection.execute_query(f"DROP TABLE resources;")
        self.connection.execute_query(f"DROP TABLE resource_type;")
        self.connection.close()


    def test_connect_success(self):
        assert self.connection.connect()

    def test_connect_failure(self):
        connection = ResourcesDataBaseManager(
            user, "wrong_password", host, 5432, database_name
        )
        assert not connection.connect()


if __name__ == "__main__":
    unittest.main()
