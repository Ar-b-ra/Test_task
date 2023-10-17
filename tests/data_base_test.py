import unittest
from data_base_manager.resource_database_manager import ResourcesDataBaseManager
from data_base_manager.resource_dataclasses import TypeResource, Resource

user = "postgres"
password = "password"
database_name = "test_db"
host = "localhost"

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


class SimpleDataBaseTests(unittest.TestCase):
    def setUp(self):
        self.db_manager = ResourcesDataBaseManager(user, password, host, 5432, database_name)
        self.db_manager.connect()
        self.db_manager.create_base_tables()
        for _type in [NO_TYPE, EXCAVATOR, TIPPER]:
            self.db_manager.create_resource_type(resource_name=_type.name, max_speed=_type.max_speed)
        for resource in [FIRST_TIPPER, SECOND_TIPPER, FIRST_EXCAVATOR, SECOND_EXCAVATOR]:
            self.db_manager.create_resource(resource_type=resource.resource_type.name,
                                            resource_name=resource.name, current_speed=resource.current_speed)

    def tearDown(self):

        self.db_manager.execute_query(f"DROP TABLE resources;")
        self.db_manager.execute_query(f"DROP TABLE resource_type;")
        self.db_manager.close()

    def test_connect_success(self):
        assert self.db_manager.connect()

    def test_connect_failure(self):
        connection = ResourcesDataBaseManager(
            user, "wrong_password", host, 5432, database_name
        )
        assert not connection.connect()

    def test_create_base_tables(self):
        # Проверка наличия таблицы "resource_type"
        self.assertIn("resource_type", self.db_manager.get_table_names())
        # Проверка наличия таблицы "resources"
        self.assertIn("resources", self.db_manager.get_table_names())

    def test_create_resource_type(self):
        test_type_1 = TypeResource(name="TestType", max_speed=100)
        self.db_manager.create_resource_type(test_type_1.name, test_type_1.max_speed)
        resource_types = self.db_manager.get_resource_types()
        # Проверка создания нового типа ресурса
        self.assertEqual(len(resource_types), 4)
        self.assertEqual(resource_types[-1], test_type_1)
        # self.assertEqual(resource_types[-1].max_speed, 100)

    def test_create_resource(self):
        test_type = TypeResource(name="TestType", max_speed=100)
        self.db_manager.create_resource_type(test_type.name, test_type.max_speed)
        test_resource = Resource(name="TestResource", current_speed=50, resource_type=test_type)
        self.db_manager.create_resource(resource_name=test_resource.name,
                                        resource_type=test_resource.resource_type.name,
                                        current_speed=test_resource.current_speed)
        resources = self.db_manager.get_resources()
        # Проверка создания нового ресурса
        self.assertEqual(len(resources), 5)
        self.assertEqual(resources[-1], test_resource)
        self.assertEqual(resources[-1].speed_exceed, 0)

    def test_get_resources(self):
        resources = self.db_manager.get_resources()
        # Проверка получения всех ресурсов

        self.assertEqual(len(resources), 4)
        self.assertEqual(resources[0].name, "101")
        self.assertEqual(resources[0].current_speed, 63)
        self.assertEqual(resources[0].resource_type, TIPPER)
        self.assertEqual(resources[0].speed_exceed, 0)
        self.assertEqual(resources[2].name, "E103")
        self.assertEqual(resources[2].current_speed, 60)
        self.assertEqual(resources[2].resource_type, EXCAVATOR)
        self.assertEqual(resources[2].speed_exceed, 50)

        # Проверка получения ресурса по имени
        resource = self.db_manager.get_resources("102")
        self.assertEqual(len(resource), 1)
        self.assertEqual(resource[0].name, "102")
        self.assertEqual(resource[0].current_speed, 85)
        self.assertEqual(resource[0].resource_type, TIPPER)
        self.assertEqual(resource[0].speed_exceed, 6)

    def test_get_resources_by_type(self):
        resources = self.db_manager.get_resources_by_type(EXCAVATOR.name)
        # Проверка получения ресурсов по типу
        self.assertEqual(len(resources), 2)
        self.assertEqual(resources[0].name, "E103")
        self.assertEqual(resources[0].current_speed, 60)
        self.assertEqual(resources[0].resource_type, EXCAVATOR)

        # Проверка получения всех ресурсов, если тип не указан
        resources = self.db_manager.get_resources_by_type()
        self.assertEqual(len(resources), 4)
        self.assertEqual(resources[0].name, "101")
        self.assertEqual(resources[0].current_speed, 63)
        self.assertEqual(resources[0].resource_type, TIPPER)
        self.assertEqual(resources[1].name, "102")
        self.assertEqual(resources[1].current_speed, 85)
        self.assertEqual(resources[1].resource_type, TIPPER)

    def test_get_resource_types(self):
        self.db_manager.create_resource_type("TestType1", 100)
        self.db_manager.create_resource_type("TestType2", 200)
        resource_types = self.db_manager.get_resource_types()
        # Проверка получения всех типов ресурсов
        self.assertEqual(len(resource_types), 5)
        self.assertEqual(resource_types[-2].name, "TestType1")
        self.assertEqual(resource_types[-2].max_speed, 100)
        self.assertEqual(resource_types[-1].name, "TestType2")
        self.assertEqual(resource_types[-1].max_speed, 200)

        # Проверка получения типа ресурса по имени
        resource_type = self.db_manager.get_resource_types("TestType1")
        self.assertEqual(len(resource_type), 1)
        self.assertEqual(resource_type[0].name, "TestType1")
        self.assertEqual(resource_type[0].max_speed, 100)

    def test_update_recourse(self):
        test_type = TypeResource(name="TestType", max_speed=100)
        self.db_manager.create_resource_type(test_type.name, test_type.max_speed)
        test_resource = Resource(name="TestResource", current_speed=50, resource_type=test_type)
        self.db_manager.create_resource(resource_name=test_resource.name,
                                        resource_type=test_resource.resource_type.name,
                                        current_speed=test_resource.current_speed)
        self.db_manager.update_recourse(test_resource.name, 80)
        resources = self.db_manager.get_resources()
        # Проверка обновления текущей скорости ресурса
        self.assertEqual(len(resources), 5)
        self.assertEqual(resources[-1].name, test_resource.name)
        self.assertEqual(resources[-1].current_speed, 80)

    def test_update_resource_type(self):
        self.db_manager.create_resource_type("TestType", 100)
        self.db_manager.update_resource_type("TestType", 150)
        resource_types = self.db_manager.get_resource_types()
        # Проверка обновления максимальной скорости типа ресурса
        self.assertEqual(len(resource_types), 4)
        self.assertEqual(resource_types[-1].name, "TestType")
        self.assertEqual(resource_types[-1].max_speed, 150)

    def test_delete_resource(self):
        self.db_manager.create_resource_type("TestType", 100)
        self.db_manager.create_resource("TestResource", "TestType", 50)
        self.db_manager.delete_resource("TestResource")
        resources = self.db_manager.get_resources()
        # Проверка удаления ресурса
        self.assertEqual(len(resources), 4)

    def test_delete_resource_type(self):
        self.db_manager.create_resource_type("TestType", 100)
        self.db_manager.create_resource("TestResource", "TestType", 50)
        self.db_manager.delete_resource_type("TestType")
        resource_types = self.db_manager.get_resource_types()
        # Проверка удаления типа ресурса
        self.assertEqual(len(resource_types), 4)


if __name__ == "__main__":
    unittest.main()
