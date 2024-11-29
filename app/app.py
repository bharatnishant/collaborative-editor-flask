from flask import Flask, request, jsonify
import redis
from crdt import CRDTDocument
from ot import OTDocument

app = Flask(__name__)
redis_client = redis.StrictRedis(host="redis", port=6379, decode_responses=True)

# Initialize CRDT and OT Documents
crdt_doc = CRDTDocument(redis_client)
ot_doc = OTDocument(redis_client)

@app.route("/crdt", methods=["GET", "POST"])
def crdt():
    if request.method == "GET":
        return jsonify({"content": crdt_doc.get_content()})
    elif request.method == "POST":
        data = request.json
        if data["type"] == "insert":
            crdt_doc.insert(data["position"], data["char"], data["client_id"])
        elif data["type"] == "delete":
            crdt_doc.delete(data["position"], data["client_id"])
        return jsonify({"status": "success", "content": crdt_doc.get_content()})

@app.route("/ot", methods=["GET", "POST"])
def ot():
    if request.method == "GET":
        return jsonify({"content": ot_doc.get_content()})
    elif request.method == "POST":
        ot_doc.apply_operation(request.json)
        return jsonify({"status": "success", "content": ot_doc.get_content()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)
