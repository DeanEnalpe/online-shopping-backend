from flask import Flask, request, jsonify, session, abort
from functools import wraps
import model.UserRequestModel as userReqModel
import model.User as userModel
from dotenv import load_dotenv
import services.UserCreation as userCreation
from flask_cors import CORS
import services.UserLogin as loginProcess
import services.ProductsRepository as products_repo
import config.SecretKey as secret_key_config
import os
import model.Products as product_model
import model.ProductsRequestModel as product_request_model
import logging
import logstash


load_dotenv()

app = Flask(__name__)
app.secret_key = secret_key_config.generate_secret_key()

origins = [
    "http://localhost:5000",
    "localhost:5000"
]

cors = CORS(app, origins=origins, supports_credentials=True, methods=["*"], allow_headers=["*"])

host = '127.0.0.1'
port = 5000

logger = logging.getLogger('python-logstash-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logstash.TCPLogstashHandler(host, port, version=1))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        is_admin = session.get('is_admin')
        if not is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        is_admin = session.get('is_admin')
        if is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@app.route('/shopping/register', methods=['POST'])
async def save_endpoint():
    userReq= userReqModel.UserRequestModel(**request.json)
    account_ = userModel.User(
                    userReq.first_name,
                    userReq.last_name,
                    userReq.email,
                    userReq.login_id,
                    userReq.password,
                    userReq.confirm_password,
                    userReq.contact_number
    )
    try:
        print("Test")
        userCreation.save_account(account_)
        logger.info('User registration attempt successful')
        return {'message': 'Successfully Registered!'}
    except Exception as e:
        logger.error('User registration attempt failed')
        return {"message": "Failed to create account"}, 400


@app.route('/shopping/login', methods=['POST'])
async def login():
    try:
        login_id = request.json.get('login_id')
        password = request.json.get('password')

        admin_is_admin = os.getenv("IS_ADMIN")
        admin_password = os.getenv("IS_ADMIN_PASSWORD")

        if login_id == admin_is_admin and password == admin_password:
            session['login_id'] = login_id
            session['is_admin'] = True
            logger.info('Admin login attempt')
            return jsonify({"message": "Admin login successful"}), 200

        login_request = loginProcess.process_login(login_id, password)
        session['login_id'] = login_request
        session['is_admin'] = False
        logger.info('User login attempt')
        return jsonify({"message": "User login successful"}), 200
    except ValueError as e:
        logger.error("An error occurred during login", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route('/shopping/products', methods=['GET'])
@user_required
def get_all_products():
    login_id = session.get('login_id')
    products = products_repo.find_all_products()
    return jsonify(login_id, products)


@app.route('/shopping/products/search', methods=['POST'])
@user_required
def get_specific_product():
    login_id = session.get('login_id')
    if not request.json or 'product_name' not in request.json:
        abort(400)
    product_name = request.json['product_name']
    try:
        product = products_repo.find_product(product_name)
        logger.info('Retrieving products')
        return jsonify({"login_id": login_id,"product": product})
    except ValueError as e:
        logger.error('Failed to retrieve products')
        return jsonify({"error": str(e)}), 404


@app.route('/shopping/admin/products', methods=['POST'])
@admin_required
def add_product():
    product_req= product_request_model.ProductsRequestModel(**request.json)
    product_ = product_model.FSEProducts(
                        product_req.product_name,
                        product_req.product_description,
                        product_req.price,
                        product_req.features,
                        product_req.quantity,
                        product_req.product_status,
                )

    try:
        print("Test")
        products_repo.save_product(product_)
        logger.info('Adding products attempted')
        return {'message': 'Product successfully added!'}
    except ValueError as e:
        logger.error('Failed to add products')
        return {"message": "Failed to add product"}, 400
    except Exception as e:
        return {"message": "Internal Server Error"}, 500


@app.route('/shopping/admin/products/<product_name>', methods=['PUT'])
@admin_required
def update_product(product_name):
    product_req = product_request_model.ProductsRequestModel(**request.json)
    product_ = product_model.FSEProducts(
                        product_req.product_name,
                        product_req.product_description,
                        product_req.price,
                        product_req.features,
                        product_req.quantity,
                        product_req.product_status,
                )

    try:
        products_repo.update_product(product_name, product_)
        logger.info('Edit products attempted')
        return {'message': 'Product successfully updated!'}
    except ValueError as e:
        logger.info('Edit products failed')
        return {"message": "Failed to update product"}, 400
    except Exception as e:
        return {"message": "Internal Server Error"}, 500