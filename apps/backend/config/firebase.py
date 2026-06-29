import os
import firebase_admin
from firebase_admin import credentials
from django.conf import settings

def initialize_firebase():
    if firebase_admin._apps:
        return

    cred_path = settings.FIREBASE_CREDENTIALS_PATH

    if not os.path.exists(cred_path):
        raise FileNotFoundError(f"Firebase service account file not found: {cred_path}")

    cred = credentials.Certificate(cred_path)

    firebase_admin.initialize_app(cred, {
        "projectId": "campusloop-94bcb",
        "storageBucket": settings.FIREBASE_STORAGE_BUCKET,
    })
