""" get items from firestore """

import functions_framework
import firebase_admin
from firebase_admin import firestore
from flask import jsonify

# Initialize Firebase Admin SDK safely
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app()

db = firestore.client()

DATABASE_NAME = "furniture-item"

@functions_framework.http
def get_items(request):
    """Fetches all items from Firestore."""
    if request.method != 'GET':
        return jsonify({"error": "Invalid request method"}), 405

    try:
        items = []
        docs = db.collection(DATABASE_NAME).stream()

        for doc in docs:
            item = doc.to_dict()
            item["id"] = doc.id  # Include Firestore document ID
            items.append(item)

        return jsonify(items), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
