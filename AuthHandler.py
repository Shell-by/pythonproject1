import jwt
import os
import datetime
import time
import hashlib
from dotenv import load_dotenv

load_dotenv()


class AuthHandler:
    public_key = os.getenv('PUBLIC_KEY')
    secret_key = os.getenv('SECRET_KEY')
    algorithm = os.getenv('ALGORITHM')
    root = os.getenv('ROOT')
    hash = hashlib.sha256()

    def encoding(self, id: str, date):
        now = time.time()
        day_second = 86400
        payload = {
            "access_key": self.public_key,
            "iss": self.root,
            "exp": now + (day_second * date),
            "iat": now,
            "id": id
        }
        json_web_token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        print(json_web_token)
