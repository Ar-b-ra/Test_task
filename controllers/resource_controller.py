import json

from db.resource_database_manager import ResourcesDataBaseManager
from logger import root_logger


class ResourceController:
    def __init__(self, data_base: ResourcesDataBaseManager):
        self.data_base = data_base

    def post(self, prepared_json):
        root_logger.info(prepared_json)
        answer = self.data_base.create_resource_type(
            resource_name=prepared_json["type"],
            max_speed=prepared_json["max_speed"],
        )
        return answer

    def get(self, prepared_json):
        answer = [
            str(json.dumps(data))
            for data in self.data_base.get_resource_types(
                resource_type_name=prepared_json.get("type")
            )
        ] if prepared_json else self.data_base.get_resource_types()

        return answer

    def update(self, prepared_json):
        answer = self.data_base.update_resource_type(resource_type=prepared_json["type"],
                                                     max_speed=prepared_json["max_speed"])
        return answer

    def delete(self, prepared_json):
        if isinstance(prepared_json, list):
            for single_json in prepared_json:
                answer = self.data_base.delete_resource_type(single_json['type'])
        else:
            answer = self.data_base.delete_resource_type(prepared_json['type'])

        return answer
