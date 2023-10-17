import json
from dataclasses import asdict

from controllers.base_resource_controller import BaseResourceController
from logger import root_logger

status = '200 OK'


class ResourceTypeController(BaseResourceController):

    def post(self, prepared_json):
        root_logger.info(prepared_json)
        answer = self.data_base.create_resource_type(
            resource_name=prepared_json["type"],
            max_speed=prepared_json["max_speed"],
        )
        return status, answer

    def get(self, prepared_json):
        answer = [json.dumps(asdict(resource)) for resource in
                  self.data_base.get_resource_types(
                resource_type_name=prepared_json.get("type"))]

        return status, answer

    def update(self, prepared_json):
        answer = self.data_base.update_resource_type(resource_type=prepared_json["type"],
                                                     max_speed=prepared_json["max_speed"])
        return status, answer

    def delete(self, prepared_json):
        if isinstance(prepared_json, list):
            for single_json in prepared_json:
                answer = self.data_base.delete_resource_type(single_json['type'])
        else:
            answer = self.data_base.delete_resource_type(prepared_json['type'])

        return status, answer
