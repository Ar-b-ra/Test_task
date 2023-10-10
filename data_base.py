import psycopg2


class DatabaseConnection:
    instance = None

    def __init__(self, dbname: str, user: str, password: str, host: str, port: int | str):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = str(port)
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("Connection to the database successful!")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)

    def create_table(self, table_name: str, primary_key: str = "id", table_params: dict = {}):
        if table_params is None:
            params_to_str = ""
        else:
            params_to_str = ", ".join([f"{key} {value}" for key, value in table_params.items()])

        self.execute_query("SELECT table_name FROM information_schema.tables "
                           "WHERE table_schema NOT IN ('information_schema','pg_catalog')")
        tables = self.cursor.fetchall()

        for table in tables:
            print(table[0])

        if table_name in [table[0] for table in tables]:
            print(f'Database witn {table_name} already exists!')
            return
        else:
            self.execute_query(f"CREATE TABLE {table_name} ("
                               f"{primary_key} SERIAL PRIMARY KEY,"
                               f"{params_to_str}"
                               f")")

    def execute_query(self, query: str):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully!")
        except (Exception, psycopg2.Error) as error:
            print("Error while executing query:", error)

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Database connection closed.")


# Пример использования класса:
if __name__ == "__main__":
    db = DatabaseConnection("Test_db", "postgres", "mysecretpassword", "localhost", 5432)
    db.connect()

    # Выполнение SQL-запроса
    db.create_table("some_table", table_params={"name": "VARCHAR(10)",
                                                "amount": "INTEGER"})

    # Закрытие соединения с базой данных
    db.close()
