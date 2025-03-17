""" get items from firestore """

import functions_framework
import firebase_admin
from firebase_admin import firestore
from flask import jsonify
from cors import set_cors_headers

# Initialize Firebase Admin SDK safely
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app()

db = firestore.client()

COLLECTION_NAME = "furniture-item"

@functions_framework.http
def get_items(request):
    """Fetches all items from Firestore."""
    if request.method == "OPTIONS":
        return set_cors_headers(''), 204
    if request.method != 'GET':
        return set_cors_headers(jsonify({"error": "Invalid request method"})), 405

    try:
        items = []
        docs = db.collection(COLLECTION_NAME).stream()

        for doc in docs:
            item = doc.to_dict()
            item["id"] = doc.id  # Include Firestore document ID
            items.append(item)

        return set_cors_headers(jsonify(items)), 200

    except Exception as e:
        return set_cors_headers(jsonify({"error": str(e)})), 500
