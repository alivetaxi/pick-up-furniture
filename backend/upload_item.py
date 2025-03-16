""" upload item """

import uuid
import os

import functions_framework
import firebase_admin
from firebase_admin import firestore, storage
from flask import jsonify


# Initialize Firebase Admin SDK safely
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app()

db = firestore.client()

BUCKET_NAME = "furniture-images"
DATABASE_NAME = "furniture-item"

@functions_framework.http
def upload_item(request):
    """Handles image uploads and stores metadata in Firestore."""
    if request.method != 'POST':
        return jsonify({"error": "Invalid request method"}), 405

    try:
        # Parse form data
        name = request.form.get("name")
        description = request.form.get("description")
        files = request.files.getlist("images")

        if not name or not description or not files:
            return jsonify({"error": "Missing fields"}), 400

        image_urls = []
        bucket = storage.bucket(BUCKET_NAME)

        # Upload each file to Cloud Storage
        for file in files:
            file_extension = file.filename.split('.')[-1]
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            blob = bucket.blob(f"uploads/{unique_filename}")
            blob.upload_from_file(file, content_type=file.content_type)
            blob.make_public()  # Make the image publicly accessible
            image_urls.append(blob.public_url)

        # Store item data in Firestore
        item_data = {
            "name": name,
            "description": description,
            "image_urls": image_urls
        }
        doc_ref = db.collection(DATABASE_NAME).add(item_data)

        return jsonify({"message": "Upload successful", "item_id": doc_ref[1].id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
