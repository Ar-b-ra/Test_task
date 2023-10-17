from typing import Union, Optional, List

from data_base_manager.resource_dataclasses import TypeResource, Resource
from data_base_manager.default_data_base import DatabaseController

TIPPER = TypeResource(name="tipper",
                      max_speed=80)
EXCAVATOR = TypeResource(name="excavator",
                         max_speed=40)
NO_TYPE = TypeResource(name="no_type",
                       max_speed=-1)

FIRST_TIPPER = Resource(
    name="101",
    current_speed=63,
    resource_type=TIPPER
)
SECOND_TIPPER = Resource(
    name="102",
    current_speed=85,
    resource_type=TIPPER
)
FIRST_EXCAVATOR = Resource(
    name="E103",
    current_speed=60,
    resource_type=EXCAVATOR
)
SECOND_EXCAVATOR = Resource(
    name="E104",
    current_speed=0,
    resource_type=EXCAVATOR
)


class ResourcesDataBaseManager(DatabaseController):
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

    def create_fixtures(self):
        for _type in [NO_TYPE, EXCAVATOR, TIPPER]:
            self.create_resource_type(resource_name=_type.name, max_speed=_type.max_speed)
        for resource in [FIRST_TIPPER, SECOND_TIPPER, FIRST_EXCAVATOR, SECOND_EXCAVATOR]:
            self.create_resource(resource_type=resource.resource_type.name,
                                 resource_name=resource.name, current_speed=resource.current_speed)

    def create_resource_type(self, resource_name: str, max_speed: int) -> bool:
        return self.execute_query(
            f"INSERT INTO resource_type (type, max_speed) VALUES('{resource_name}', {max_speed})"
        )

    def create_resource(
            self, resource_name: str, resource_type: Union[str, int], current_speed: int
    ) -> bool:
        if isinstance(resource_type, str):
            resource_type_id = self._get_resource_type_id(resource_type)
        else:
            resource_type_id = resource_type
        return self.execute_query(
            f"INSERT INTO resources (name, resource_type_id, cur_speed) "
            f"VALUES(\'{resource_name}\', {resource_type_id}, {current_speed})"
        )

    def get_resources(self, resource_name: Optional[str] = None) -> list[Resource]:
        if resource_name:
            self.execute_query(f"SELECT * FROM resources WHERE name=\'{resource_name}\'")
        else:
            self.execute_query(r"SELECT * FROM resources")
        resources = self.cursor.fetchall()
        answer = []
        types = {}
        for _, res_type_id, name, cur_speed in resources:
            if not (resource_type := types.get(res_type_id)):
                resource_type = self._get_resource_type_by_id(res_type_id)
                types[res_type_id] = resource_type
            answer.append(
                Resource(
                    name=name,
                    current_speed=cur_speed,
                    resource_type=resource_type
                )
            )
        return answer

    def get_resources_by_type(self, resource_type: Optional[str] = None) -> list[Resource]:
        resource_type_id = self._get_resource_type_id(resource_type=resource_type) if resource_type else None
        if resource_type_id:
            self.execute_query(
                f"SELECT * FROM resources WHERE resource_type_id=\'{resource_type_id}\'"
            )
        else:
            self.execute_query(r"SELECT * FROM resources")
        answer = []
        types = {}
        resources = self.cursor.fetchall()
        for _, res_type_id, name, cur_speed in resources:
            if not (resource_type := types.get(res_type_id)):
                resource_type = self._get_resource_type_by_id(res_type_id)
                types[res_type_id] = resource_type
            answer.append(
                Resource(
                    name=name,
                    current_speed=cur_speed,
                    resource_type=resource_type
                )
            )
        return answer

    def get_resource_types(self, resource_type_name: Optional[str] = None) -> list[TypeResource]:
        if resource_type_name:
            self.execute_query(
                f"SELECT * FROM resource_type WHERE type=\'{resource_type_name}\'"
            )
        else:
            self.execute_query(f"SELECT * FROM resource_type")
        resource_types = self.cursor.fetchall()
        return [
            TypeResource(
                name=res_type,
                max_speed=max_speed
            )
            for _, res_type, max_speed in resource_types
        ]

    def update_recourse(self, resource_name: str, current_speed: int) -> bool:
        return self.execute_query(
            f"UPDATE resources SET cur_speed = {current_speed} WHERE name = '{resource_name}'")

    def update_resource_type(self, resource_type: str, max_speed: int) -> bool:
        return self.execute_query(f"UPDATE resource_type SET max_speed = {max_speed} WHERE type = '{resource_type}'")

    def delete_resource(self, resource_name: str) -> bool:
        return self.delete_rows(table="resources", condition=f"name=\'{resource_name}\'")

    def delete_resource_type(self, resource_type_name: str) -> bool:
        resource_type_id = self._get_resource_type_id(resource_type_name)
        self.execute_query(
            f"UPDATE resources "
            f"SET resource_type_id = -1 "
            f"WHERE resource_type_id={resource_type_id}"
        )
        return self.delete_rows(table="resource_type", condition=f"type=\'{resource_type_name}\'")

    def _get_resource_type_id(self, resource_type: str) -> int:
        self.execute_query(f"SELECT id FROM resource_type WHERE type='{resource_type}'")
        (resource_type_id,) = self.cursor.fetchone()
        return resource_type_id

    def _get_resource_type_by_id(self, resource_type_id: int) -> TypeResource:
        self.execute_query(
            f"SELECT type, max_speed FROM resource_type WHERE id='{resource_type_id}'"
        )
        (
            resource_type,
            max_speed,
        ) = self.cursor.fetchone()
        return TypeResource(name=resource_type, max_speed=max_speed)
