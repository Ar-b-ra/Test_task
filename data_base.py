from typing import Union
import psycopg2
from logger import root_logger


class DatabaseConnection:
    instance = None

    def __init__(
            self, user: str, password: str, host: str, port: Union[int, str], dbname: str = None
    ):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = str(port)
        self.connection = None
        self.cursor = None

    def connect(self) -> bool:
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            self.cursor = self.connection.cursor()
            self.connection.autocommit = True
            root_logger.success("Connection to the database successful!")
            return True
        except psycopg2.Error as error:
            root_logger.critical(f"Error while connecting to PostgresSQL: {error}")
            return False

    def create_table(
            self, table_name: str, primary_key: str = "id", foreign_key: tuple = None, table_params: dict = None
    ):
        root_logger.debug(f"Creating table with {table_name = }, {foreign_key = } and {table_params = }")
        if table_params is None:
            params_to_str = ""
        else:
            params_to_str = ", ".join(
                [f"{key} {value}" for key, value in table_params.items()]
            )

        self.execute_query(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema NOT IN ('information_schema','pg_catalog')"
        )
        tables = self.cursor.fetchall()

        root_logger.debug([table[0] for table in tables])

        if table_name in [table[0] for table in tables]:
            root_logger.warning(f"Database with {table_name = } already exists!")
            return
        else:
            if foreign_key:
                _key, ref_table, ref_param = foreign_key
                self.execute_query(
                    f"""CREATE TABLE {table_name} ("""
                    f"""{primary_key} SERIAL PRIMARY KEY,"""
                    f"""{_key} integer REFERENCES {ref_table}({ref_param}),"""
                    f"{params_to_str}"""
                    f""")"""
                )
            else:
                self.execute_query(
                    f"""CREATE TABLE {table_name} ("""
                    f"""{primary_key} SERIAL PRIMARY KEY,"""
                    f"{params_to_str}"""
                    f""")"""
                )

    def create_database(self, db_name: str):
        root_logger.debug(f"Creating database with {db_name = }")
        self.execute_query(
            f"""CREATE DATABASE {db_name}"""
        )

    def delete_rows(self, table: str, condition: str):
        delete_query = f"""
            DELETE FROM {table} WHERE {condition};
        """
        self.execute_query(delete_query)

    def execute_query(self, query: str):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            root_logger.success("Query executed successfully!")
        except psycopg2.Error as error:
            root_logger.critical(f"Error while executing query: {error}")

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            root_logger.success("Database connection closed.")


# Подготовка БД
if __name__ == "__main__":
    def prepare_db() -> DatabaseConnection:
        test_db = "test_db"
        db = DatabaseConnection(
            dbname=test_db, user="postgres", password="password", host="localhost", port=5432
        )
        is_success_connection = db.connect()
        if not is_success_connection:
            db.dbname = None
            db.connect()
            db.create_database(test_db)
            db.dbname = test_db
            db.connect()

        db.create_table(
            table_name="resource_type", table_params={"type": "VARCHAR(10)", "max_speed": "INTEGER"}
        )
        db.create_table(
            table_name="resource", foreign_key=("resource_type_id", "resource_type", "id"),
            table_params={
                "name": "VARCHAR(10)",
                "cur_speed": "INTEGER",
                "max_speed_exceeding": "INTEGER"
            }
        )
        db.close()
        return db


    data_base = prepare_db()
