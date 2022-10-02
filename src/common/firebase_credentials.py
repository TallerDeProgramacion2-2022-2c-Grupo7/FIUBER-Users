import os
import json
from base64 import b64decode

try:
    _json_str = b64decode(os.environ["FIREBASE_CREDENTIALS"]).decode()
    admin_credentials = json.loads(_json_str)
except KeyError:
    admin_credentials = "firebase_credentials.json"
