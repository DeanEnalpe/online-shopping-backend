from pymongo import MongoClient
import os
from dotenv import load_dotenv
from model.Products import FSEProducts
import pandas as pd
import re
from flask import jsonify
load_dotenv()

client = MongoClient(os.getenv("MONGODB_URL"))
db = client["mongodb"]
collection = db["fseproducts"]


def products_to_dictionary():
    directory = 'C:/Users/2236561/PycharmProjects/online-shopping-backend-fse/resources/new_products.csv'
    if not os.path.exists(directory):
        raise FileNotFoundError(f"{directory} does not exist.")
    data = pd.read_csv(directory)
    products_df = pd.DataFrame(data)
    products_dict = products_df.to_dict(orient="records")
    return collection.insert_many(products_dict)


def find_all_products():
    if collection.count_documents({}) == 0:
        products_to_dictionary()

    products = list(collection.find({}, {"_id": 0}))

    products_objects = []
    for product in products:
        if 'quantity' in product:
            products_objects.append(FSEProducts(
                product_name=product['product_name'],
                product_description=product['product_description'],
                price=product['price'],
                features=product['features'],
                quantity=product['quantity'],
                product_status=product['product_status']
            ))

    products_dict = [product.convert_to_json() for product in products_objects]
    return products_dict


def find_product(product_name):
    product = collection.find_one({"product_name": product_name}, {"_id": 0})
    if product:
        if product['product_status'] == 'HURRY UP TO PURCHASE':
            return product
        if product['product_status'] == 'OUT OF STOCK':
            raise ValueError('OUT OF STOCK')
    else:
        if collection.count_documents({}) == 0:
            products_to_dictionary()
            product = collection.find_one({"product_name": product_name}, {"_id": 0})
            if product:
                if product['product_status'] == 'HURRY UP TO PURCHASE':
                    return product
                if product['product_status'] == 'OUT OF STOCK':
                    raise ValueError('OUT OF STOCK')
        return None


def validate_product_status(product_status, quantity):
    error_msg = ""

    if quantity == 0:
        if product_status not in ['OUT OF STOCK', 'HURRY UP TO PURCHASE']:
            error_msg = "Product status should only be 'OUT OF STOCK' or 'HURRY UP TO PURCHASE'."

    if len(error_msg) > 0:
        error_msg = "Error! " + error_msg
        return {"message": error_msg}


def validate_price(price):
    pattern = r'^(?:0(?:\.[0-9]{1,2})?|1(?:\.00?)?)$'
    error_msg = ""

    if not re.match(pattern, price):
        error_msg = "Price should only contain numbers and have exactly 2 decimal places."

    if len(error_msg) > 0:
        error_msg = "Error! " + error_msg
        return {"message": error_msg}


def validate_quantity(quantity):
    pattern = r"^0|[1-9]\d*$"
    error_msg = ""

    if not re.match(pattern, quantity):
        error_msg = "Quantity should only contain numbers."

    if len(error_msg) > 0:
        error_msg = "Error! " + error_msg
        return {"message": error_msg}


def validate_product(product):
    validate_price(product.price)
    validate_quantity(product.quantity)
    validate_product_status(product.product_status, product.quantity)


def save_product(product):
    validate_product(product)
    new_product = collection.insert_one(product.convert_to_json())
    created_product = collection.find_one({"_id" : new_product.inserted_id})

    if created_product is None:
        return None
    else:
        return product


def update_product(product_name, updated_product):
    validate_product(updated_product)
    existing_product = collection.find_one({"product_name": product_name})
    if existing_product:
        collection.update_one({"product_name": product_name}, {"$set": updated_product.convert_to_json()})
        # updated_product = collection.find_one({"product_name": updated_product.product_name}, {"_id": 0})
        # return updated_product
    else:
        return {"message": "Product not found"}
