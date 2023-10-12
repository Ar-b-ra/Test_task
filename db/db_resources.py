from db.data_base import DatabaseConnection


class ResourcesDataBaseManager(DatabaseConnection):
    def prepare_test_db(self, test_db_name: str = "test_db"):
        self.dbname = test_db_name
        is_success_connection = self.connect()
        if not is_success_connection:
            self.dbname = None
            self.connect()
            self.create_database(test_db_name)
            self.dbname = test_db_name
            self.connect()

    def create_base_tables(self):
        self.create_table(
            table_name="resource_type",
            table_params={"type": "VARCHAR(20)", "max_speed": "INTEGER"},
        )
        self.create_table(
            table_name="resources",
            foreign_key=("resource_type_id", "resource_type", "id"),
            table_params={
                "name": "VARCHAR(20)",
                "cur_speed": "INTEGER",
            },
        )

    def get_resources(self, resource_name: str = None) -> list:
        if resource_name:
            self.execute_query(f"SELECT * FROM resources WHERE name='{resource_name}'")
        else:
            self.execute_query(r"SELECT * FROM resources")
        resources = self.cursor.fetchall()
        answer = []
        types = {}
        for _, res_type_id, name, cur_speed in resources:
            if not (type_params := types.get(res_type_id)):
                type_params = self._get_resource_type_by_id(res_type_id)
                types[res_type_id] = type_params
            res_type, max_speed = type_params
            answer.append(
                {
                    "name": name,
                    "cur_speed": cur_speed,
                    "type": res_type,
                    "speed_exceed": int((cur_speed - max_speed)/max_speed * 100)
                    if cur_speed > max_speed
                    else 0,
                }
            )
        return answer

    def get_resources_by_type(self, resource_type: str = None) -> list:
        resource_type_id = self._get_resource_type_id(resource_type=resource_type)
        if resource_type_id:
            self.execute_query(
                f"SELECT * FROM resources WHERE resource_type_id='{resource_type_id}'"
            )
        else:
            self.execute_query(r"SELECT * FROM resources")
        return self.cursor.fetchall()

    def get_resource_types(self, resource_type_name: str = None) -> list:
        if resource_type_name:
            self.execute_query(
                f"SELECT id FROM resource_type WHERE type='{resource_type_name}'"
            )
        else:
            self.execute_query(f"SELECT * FROM resource_type")
        resource_types = self.cursor.fetchall()
        return [
            {"type": res_type, "max_speed": max_speed}
            for _, res_type, max_speed in resource_types
        ]

    def create_resource_type(self, resource_name: str, max_speed: int):
        self.execute_query(
            f"INSERT INTO resource_type (type, max_speed) VALUES('{resource_name}', {max_speed})"
        )

    def create_resource(
        self, resource_name: str, resource_type: str | int, current_speed: int
    ):
        if isinstance(resource_type, str):
            resource_type_id = self._get_resource_type_id(resource_type)
        else:
            resource_type_id = resource_type
        self.execute_query(
            f"INSERT INTO resources (name, resource_type_id, cur_speed) "
            f"VALUES('{resource_name}', {resource_type_id}, {current_speed})"
        )

    def remove_resource(self, resource_name: str):
        self.delete_rows(table="resources", condition=f"name={resource_name}")

    def remove_resource_type(self, resource_type_name: str):
        resource_type_id = self._get_resource_type_id(resource_type_name)
        self.execute_query(
            f"UPDATE resources "
            f"SET resource_type = -1 "
            f"WHERE resource_type_id={resource_type_id}"
        )
        self.delete_rows(table="resource_type", condition=f"type={resource_type_name}")

    def _get_resource_type_id(self, resource_type: str) -> int:
        self.execute_query(f"SELECT id FROM resource_type WHERE type='{resource_type}'")
        (resource_type_id,) = self.cursor.fetchone()
        return resource_type_id

    def _get_resource_type_by_id(self, resource_type_id: int) -> tuple[str, int]:
        self.execute_query(
            f"SELECT id, max_speed FROM resource_type WHERE id='{resource_type_id}'"
        )
        (
            resource_type,
            max_speed,
        ) = self.cursor.fetchone()
        return resource_type, max_speed
