#!/usr/bin/env python3

# Standard library imports

# Remote library imports
import os
from flask import Flask, jsonify, request, make_response, session,render_template

from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from dotenv import load_dotenv
load_dotenv()


# Local imports
from models import db, User, Product, ProductItem

# Instantiate app, set attributes
app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/build',
    template_folder='../client/build'
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "Key"
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# Instantiate REST API
api = Api(app)

# Instantiate CORS
CORS(app)

# Define home route
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pantry Pal API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 800px;
                margin: 50px auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
            }
            p {
                margin-bottom: 15px;
            }
            ul {
                list-style-type: none;
                padding-left: 20px;
            }
            li {
                margin-bottom: 5px;
            }
            a {
                color: #007bff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to Pantry Pal API</h1>
            <p>This is the API for Pantry Pal application.</p>
            <p>Endpoints:</p>
            <ul>
                <li><strong>/users</strong> -:GET - List of all users details</li>
                <li><strong>/users</strong> -:POST - Sign up a new user</li>
                <li><strong>/users/int:id</strong> -:GET - Get a user details</li>
                <li><strong>/users/int:id</strong> -:PATCH - Update a user details</li>
                <li><strong>/users/int:id</strong> -:DELETE - Delete a user</li>
                <li><strong>/login</strong> -:POST - User login</li>
                <li><strong>/logout</strong> -:DELETE - User logout</li>
                <li><strong>/check_session</strong>:GET - Check user session</li>
                <li><strong>/products</strong>:GET - List of all products</li>
                <li><strong>/products</strong>:POST - Create a new product</li>
                <li><strong>/products/int:id</strong>:GET - Get a specific product</li>
                <li><strong>/products/int:id</strong>:PATCH - Update a specific product</li>
                <li><strong>/products/int:id</strong>:DELETE - Delete a specific product</li>
                <li><strong>/product_items</strong>:GET - List of all product items</li>
                <li><strong>/product_items</strong>:POST - Create a new product item</li>
                <li><strong>/product_items/int:id</strong>:GET - Get a specific product item</li>
                <li><strong>/product_items/int:id</strong>:PATCH - Update a specific product item</li>
                <li><strong>/product_items/int:id</strong>:DELETE - Delete a specific product item</li>
            </ul>
        </div>
    </body>
    </html>
    """

class Users(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(jsonify(users), 200)

    def post(self):
        data = request.get_json()

        # Check if the email or username already exists
        existing_user = User.query.filter(
            (User.email == data['email']) | (User.username == data['username'])
        ).first()

        if existing_user:
            error_message = 'Email already exists' if existing_user.email == data['email'] else 'Username already exists'
            return make_response(jsonify({'error': error_message}), 400)

        # Create a new user
        new_user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],  # Use password property
            picture=data.get('picture')  # Optionally allow picture to be provided
        )

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return make_response(jsonify(new_user.to_dict()), 201)

api.add_resource(Users, '/users')



class UserByID(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(user), 200)

    def patch(self, id):
        user = User.query.filter_by(id=id).first()
        data = request.get_json()

        for key, value in data.items():
            setattr(user, key, value)

        db.session.commit()

        return make_response(jsonify(user.to_dict()), 200)

    def delete(self, id):
        user = User.query.filter_by(id=id).first()

        db.session.delete(user)
        db.session.commit()

        return '', 204


api.add_resource(UserByID, '/users/<int:id>')

class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email: 
            return {'message': 'Email is required'}, 400
        
        if not password:
            return {'message': 'Password is required'}, 400
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            return {'error': 'Email not found'}, 404
        
        if user.check_password(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        
        return {'error': 'Invalid password'}, 401


class Logout(Resource):
    def delete(self):
        if 'user_id' in session:
            session.pop('user_id')
        return '', 204

class CheckSession(Resource):
    def get(self):
        if 'user_id' in session:
            user_id = session['user_id']
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200  # Return a dictionary instead of a Response object
            else:
                return {'message': 'User not found'}, 404
        else:
            return {'message': 'Unauthorized'}, 401  # Return a dictionary instead of an empty string


# Add resources to the API
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')


# Product Resources
class Products(Resource):
    def get(self):
        products = [product.to_dict() for product in Product.query.all()]
        return make_response(jsonify(products), 200)

    def post(self):
        data = request.get_json()

        # Create a new product
        new_product = Product(
            name=data['name'],
            user_id=data['user_id'],
            category=data['category'],
            storage_place=data['storage_place'],
            quantity=data.get('quantity', 0),
            unit=data['unit'],
            low_limit=data.get('low_limit', 0)  # Set default value if not provided
        )

        # Add the new product to the database
        db.session.add(new_product)
        db.session.commit()

        return make_response(jsonify(new_product.to_dict()), 201)

api.add_resource(Products, '/products')


class ProductByID(Resource):
    def get(self, id):
        product = Product.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(product), 200)

    def patch(self, id):
        product = Product.query.filter_by(id=id).first()
        data = request.get_json()

        for key, value in data.items():
            setattr(product, key, value)

        db.session.commit()

        return make_response(jsonify(product.to_dict()), 200)

    def delete(self, id):
        product = Product.query.filter_by(id=id).first()

        db.session.delete(product)
        db.session.commit()

        return '', 204

api.add_resource(ProductByID, '/products/<int:id>')


# ProductItem Resources
class ProductItems(Resource):
    def get(self):
        product_items = [item.to_dict() for item in ProductItem.query.all()]
        return make_response(jsonify(product_items), 200)

    def post(self):
        data = request.get_json()

        # Create a new product item
        new_product_item = ProductItem(
            product_id=data['product_id'],
            brand_name=data['brand_name'],
            quantity=data['quantity'],
            expiry_date=data.get('expiry_date')
        )

        # Add the new product item to the database
        db.session.add(new_product_item)
        db.session.commit()

        return make_response(jsonify(new_product_item.to_dict()), 201)

api.add_resource(ProductItems, '/product_items')

class ProductItemByID(Resource):
    def get(self, id):
        product_item = ProductItem.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(product_item), 200)

    def patch(self, id):
        product_item = ProductItem.query.filter_by(id=id).first()
        data = request.get_json()

        for key, value in data.items():
            setattr(product_item, key, value)

        db.session.commit()

        return make_response(jsonify(product_item.to_dict()), 200)

    def delete(self, id):
        product_item = ProductItem.query.filter_by(id=id).first()

        db.session.delete(product_item)
        db.session.commit()

        return '', 204

api.add_resource(ProductItemByID, '/product_items/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)