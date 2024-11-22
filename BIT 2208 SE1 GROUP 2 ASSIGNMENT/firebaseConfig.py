import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import firestore

cred = credentials.Certificate("tuckshopmobileapp-firebase-adminsdk-7gf70-6f88e64290.json")
firebase_admin.initialize_app(cred)

db=firestore.client()