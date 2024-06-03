from pymongo import MongoClient
import os
import re
import bcrypt
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URL"))
db = client["mongodb"]
collection = db["users"]


def validate_first_name(first_name):
    pattern = re.compile("^[a-zA-Z0-9_]+$")
    error_msg = ""

    if len(first_name) > 20 or len(first_name) < 4:
        error_msg = "First Name should have at least 4 characters with a maximum of 20 characters."

    if not pattern.match(first_name):
        error_msg = error_msg + ("First name should only have either a series of alphabet with numbers or an _. "
                                 "No other special characters allowed.")

    if len(error_msg) > 0:
        error_msg = "Error!" + error_msg
        raise ValueError(error_msg)
    else:
        return "Valid!"


def validate_last_name(last_name):
    pattern = re.compile("^[a-zA-Z0-9_]+$")
    error_msg = ""

    if len(last_name) > 20 or len(last_name) < 4:
        error_msg = "Last name should have at least 4 characters with a maximum of 20 characters."

    if not pattern.match(last_name):
        error_msg = error_msg + ("Last name should only have either a series of alphabet with numbers or an _. "
                                 "No other special characters allowed.")

    if len(error_msg) > 0:
        error_msg = "Error!" + error_msg
        raise ValueError(error_msg)
    else:
        return "Valid!"


def validate_login_id(login_id):
    error_msg = ""
    login_id_existing_count = collection.count_documents({"login_id": login_id})

    if login_id_existing_count > 0:
        error_msg = "Login ID already exist"
    if len(login_id) > 20 or len(login_id) < 4:
        error_msg = "Login ID should have at least 4 characters with a maximum of 20 characters."

    if len(error_msg) > 0:
        error_msg = "Error!" + error_msg
        raise ValueError(error_msg)
    else:
        return "Valid!"


def validate_email(email):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    error_msg = ""

    accounts_existing_count = collection.count_documents({"email": email})
    if accounts_existing_count > 0:
        error_msg = "Email already exists. "
    if not re.match(pattern,email):
        error_msg += "Email should be format like this: abc_123@site.com"

    if len(error_msg) > 0:
        error_msg = "Error! "
        raise ValueError(error_msg)


def validate_password(password):
    # pattern = re.compile("^.*(?=.{8,})(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!#$%&?_]).*$")
    error_msg = ""
    if len(password) > 20 or len(password) < 8:
        error_msg = "Password should have at least 8 characters with a maximum of 20 characters. "
    #
    # if not pattern.match(password):
    #     print("Password validation failed:", password)
    #     error_msg = error_msg + ("Password should contain at least 1 uppercase letter, 1 digit, "
    #                              "and 1 of the special characters: !#$%&?_")

    if len(error_msg) > 0:
        error_msg = "Error! " + error_msg
        raise ValueError(error_msg)


def validate_confirm_password(password, confirm_password):
    if password != confirm_password:
        raise ValueError("Error! Password and confirm password do not match.")


def validate_contact_number(contact_number):
    # pattern = r"^09\d+$"
    error_msg = ""
    if len(contact_number) > 11:
        error_msg = "Mobile number exceeds 11 characters"

    if len(contact_number) < 11:
        error_msg = "Contact number is less than 11 characters"

    # if not re.match(pattern, contact_number):
    #     error_msg = error_msg + "Contact number should be format like this: 09123456789"

    if len(error_msg) > 0:
        error_msg = "Error! "
        raise ValueError(error_msg)


def validate_account(users):
    validate_first_name(users.first_name)
    validate_last_name(users.last_name)
    validate_email(users.email)
    validate_login_id(users.login_id)
    validate_password(users.password)
    validate_confirm_password(users.password, users.confirm_password)
    validate_contact_number(users.contact_number)


def save_account(users):
    validate_account(users)
    hashed_password = bcrypt.hashpw(users.password.encode('utf-8'), bcrypt.gensalt())
    users.password = hashed_password.decode('utf-8')  # Decode the hashed password
    new_acc = collection.insert_one(users.convert_to_json())
    created_acc = collection.find_one({"_id" : new_acc.inserted_id})

    if created_acc is None:
        return None
    else:
        return users