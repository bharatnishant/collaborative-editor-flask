import redis
import json

class CRDTDocument:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.operations_key = "crdt_operations"
        self.document_key = "crdt_content"
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

    def insert(self, position, char, client_id):
        operation = {"type": "insert", "position": position, "char": char, "client_id": client_id}
        self.apply_operation(operation)

    def delete(self, position, client_id):
        operation = {"type": "delete", "position": position, "client_id": client_id}
        self.apply_operation(operation)

    def apply_operation(self, operation):
        operations = self.get_operations()
        if operation not in operations:
            operations.append(operation)
            content = self.get_content()
            if operation["type"] == "insert":
                content.insert(operation["position"], operation["char"])
            elif operation["type"] == "delete" and operation["position"] < len(content):
                content.pop(operation["position"])
            self.redis_client.set(self.operations_key, json.dumps(operations))
            self.redis_client.set(self.document_key, json.dumps(content))
