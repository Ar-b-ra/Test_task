import json
from dataclasses import asdict

from controllers.base_resource_controller import BaseResourceController

status = '200 OK'


class ResourceController(BaseResourceController):

    def post(self, prepared_json):
        answer = self.data_base.create_resource(resource_name=prepared_json["name"],
                                                resource_type=prepared_json["type"],
                                                current_speed=prepared_json["speed"])
        return status, answer

    def get(self, prepared_json):
        answer = [json.dumps(asdict(resource)) for resource in
                  self.data_base.get_resources(resource_name=prepared_json.get("name"))]
        return status, answer

    def update(self, prepared_json):
        answer = self.data_base.update_recourse(resource_name=prepared_json["name"],
                                                current_speed=prepared_json["cur_speed"])
        return status, answer

    def delete(self, prepared_json):
        answer = self.data_base.delete_resource(resource_name=prepared_json['name'])
        return status, answer
