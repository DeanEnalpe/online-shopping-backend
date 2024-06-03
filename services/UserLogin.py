from pymongo import MongoClient
import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URL"))
db = client["mongodb"]
collection = db["users"]

def check_password(current_pw, pw_entered):
    return bcrypt.checkpw(pw_entered.encode('utf-8'), current_pw)


def process_login(login_id, password):
    created_acc = collection.find_one({"login_id": login_id})
    if created_acc is not None:
        is_valid_pass = check_password(created_acc.get('password').encode('utf-8'), password)
    else:
        raise ValueError("User does not exist")

    if is_valid_pass:
        return created_acc.get('login_id')
    else:
        raise ValueError("Wrong password")

