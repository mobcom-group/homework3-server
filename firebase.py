
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("mobcom-f1a53-firebase-adminsdk-2dkvm-45db9d6f3c.json")
firebase_admin.initialize_app(cred)
