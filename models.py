from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, UniqueConstraint
import re
from sqlalchemy.ext.hybrid import hybrid_property
from flask_bcrypt import Bcrypt



# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
bcrypt = Bcrypt()


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-products.user',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=True)
    # Define relationship
    products = db.relationship('Product', back_populates='user', cascade='all, delete, delete-orphan') 
    
    def __repr__(self):
        return f'<User {self.username} | Email: {self.email}>'
    
    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise ValueError('Username is required')
        if len(username) > 50:
            raise ValueError('Username must be less than 50 characters')
        return username
    
    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise ValueError('Email is required')
        
        # Check email format using regular expression
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            raise ValueError('Invalid email format')

        return email
    
    @hybrid_property
    def password(self):
        return self._password_hash

    @password.setter
    def password(self, plaintext_password):
        self._password_hash = bcrypt.generate_password_hash(plaintext_password).decode('utf-8')

    def check_password(self, plaintext_password):
        return bcrypt.check_password_hash(self._password_hash, plaintext_password)
    
class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'

    serialize_rules = ('-user.products','-product_items.product')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    storage_place = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=True) 
    unit = db.Column(db.String(20), nullable=False)
    low_limit = db.Column(db.Integer, nullable=True)

    # relationships
    user = db.relationship('User', back_populates='products')
    product_items = db.relationship('ProductItem', back_populates='product', cascade='all, delete, delete-orphan')

     # Composite unique constraint
    __table_args__ = (UniqueConstraint('name', 'user_id', name='unique_product_per_user'),)

    def __repr__(self):
        return f'<Product {self.name}| Category: {self.category} | Storage Place: {self.storage_place} | Quantity: {self.quantity}>'

class ProductItem(db.Model, SerializerMixin):
    __tablename__ = 'product_items'

    serialize_rules = ('-product.product_items',)

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    brand_name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    expiry_date = db.Column(db.Date, nullable=True)

    # relationships
    product = db.relationship('Product', back_populates='product_items')

    def __repr__(self):
        return f'<ProductItem {self.brand_name} | Quantity: {self.quantity} | Expiry Date: {self.expiry_date}>'
    