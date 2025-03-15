""" flask app to get items from firestore """

import base64
import uuid

from flask import Flask, jsonify, request
from google.cloud import storage,firestore

app = Flask(__name__)

storage_client = storage.Client()
firestore_client = firestore.Client()

BUCKET_NAME = "furniture-images"
DATABASE_NAME = "furniture-item"

@app.route('/upload-item', methods=['POST'])
def upload_item():
    """ upload item to firestore """

    data = request.json
    name = data.get("name")
    description = data.get("description")
    images = data.get("images", [])

    if not name or not images:
        return jsonify({"error": "Missing required fields"}), 400

    image_urls = []
    for image_data in images:
        image_id = str(uuid.uuid4())
        image_bytes = base64.b64decode(image_data)
        blob = storage_client.bucket(BUCKET_NAME).blob(f"images/{image_id}.jpg")
        blob.upload_from_string(image_bytes, content_type="image/jpeg")
        image_urls.append(blob.public_url)

    # 存入 Firestore
    doc_ref = firestore_client.collection(DATABASE_NAME).document()
    doc_ref.set({
        "name": name,
        "description": description,
        "image_urls": image_urls
    })

    return jsonify({"message": "Upload successful", "image_urls": image_urls})



@app.route('/get-items', methods=['GET'])
def get_items():
    """ get items from firestore """

    items_ref = firestore_client.collection(DATABASE_NAME)
    docs = items_ref.stream()

    items = []
    for doc in docs:
        item = doc.to_dict()
        items.append({
            "id": doc.id,
            "name": item.get("name"),
            "description": item.get("description"),
            "image_urls": item.get("image_urls", [])
        })

    return jsonify(items)


def main(req):
    """ main function """

    return app(req)
