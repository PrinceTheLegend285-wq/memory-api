from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["prince_ai"]

memory = db["memory"]

@app.route("/")
def home():
    return "Memory API Running"

# Save message
@app.route("/save", methods=["POST"])
def save():

    data = request.json

    memory.insert_one({
        "user_id": data["user_id"],
        "role": data["role"],
        "content": data["content"]
    })

    return jsonify({
        "status": "saved"
    })

# Get memory
@app.route("/memory/<user_id>")
def get_memory(user_id):

    chats = list(
        memory.find(
            {"user_id": user_id},
            {"_id": 0}
        ).sort("_id", -1).limit(10)
    )

    chats.reverse()

    return jsonify(chats)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)