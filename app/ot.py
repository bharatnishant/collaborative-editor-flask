import redis
import json

class OTDocument:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.operations_key = "ot_operations"
        self.document_key = "ot_content"
        self.initialize_redis()

    def initialize_redis(self):
        if not self.redis_client.exists(self.document_key):
            self.redis_client.set(self.document_key, json.dumps([]))
        if not self.redis_client.exists(self.operations_key):
            self.redis_client.set(self.operations_key, json.dumps([]))

    def get_content(self):
        return json.loads(self.redis_client.get(self.document_key))

    def get_operations(self):
        return json.loads(self.redis_client.get(self.operations_key))

    def apply_operation(self, operation):
        operations = self.get_operations()
        for existing_op in operations:
            operation = self.transform(operation, existing_op)
        self.execute_operation(operation)
        operations.append(operation)
        self.redis_client.set(self.operations_key, json.dumps(operations))

    def execute_operation(self, operation):
        content = self.get_content()
        if operation["type"] == "insert":
            content.insert(operation["position"], operation["char"])
        elif operation["type"] == "delete" and operation["position"] < len(content):
            content.pop(operation["position"])
        self.redis_client.set(self.document_key, json.dumps(content))

    def transform(self, new_op, existing_op):
        if existing_op["type"] == "insert" and existing_op["position"] <= new_op["position"]:
            new_op["position"] += 1
        elif existing_op["type"] == "delete" and existing_op["position"] < new_op["position"]:
            new_op["position"] -= 1
        return new_op
