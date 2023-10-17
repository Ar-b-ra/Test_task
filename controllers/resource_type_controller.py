from db.resource_database_manager import ResourcesDataBaseManager


class ResourceTypeController:
    def __init__(self, data_base: ResourcesDataBaseManager):
        self.data_base = data_base

    def post(self, prepared_json):
        answer = self.data_base.create_resource(resource_name=prepared_json["name"],
                                                resource_type=prepared_json["type"],
                                                current_speed=prepared_json["speed"])
        return answer

    def get(self, prepared_json):
        answer = self.data_base.get_resources(resource_name=prepared_json.get("name"))
        return answer

    def update(self, prepared_json):
        answer = self.data_base.update_recourse(resource_name=prepared_json["name"],
                                                current_speed=prepared_json["cur_speed"])
        return answer

    def delete(self, prepared_json):
        answer = self.data_base.delete_resource(resource_name=prepared_json['name'])
        return answer
