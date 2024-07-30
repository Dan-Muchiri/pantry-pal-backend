#!/usr/bin/env python3

# Standard library imports
from random import randint, choice
from faker import Faker

# Local imports
from app import app, db  # Import Flask app and db instance
from models import User, Product  # Import User and Product models

if __name__ == '__main__':
    fake = Faker()
    
    # Initialize Flask app context
    with app.app_context():
        print("Starting seed...")
        
        # Clear existing data (optional)
        db.drop_all()
        db.create_all()
        
        # Seed users
        users = []
        for _ in range(4):
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                picture="https://picsum.photos/983/458" # Add a fake picture URL for each user
            )
            users.append(user)
        
        dan = User(
            username='dan',
            email='danspmunene@gmail.com',
            password="munene",
            picture="https://picsum.photos/983/458" # Add a fake picture URL for each user 
        )
        users.append(dan)

        for user in users:
            db.session.add(user)

        db.session.commit()
        
        # Category-Product Mappings
        category_product_map = {
            'Fruits': ['Apple', 'Banana', 'Orange', 'Grapes'],
            'Vegetables': ['Carrot', 'Broccoli', 'Spinach', 'Potato'],
            'Dairy': ['Milk', 'Cheese', 'Yogurt', 'Butter'],
            'Meat': ['Chicken Breast', 'Beef Steak', 'Pork Chops', 'Ground Beef'],
            'Beverages': ['Orange Juice', 'Coffee', 'Tea', 'Soda']
        }
        
        # Storage Places Mapping
        category_storage_map = {
            'Fruits': ['Pantry', 'Fridge'],
            'Vegetables': ['Pantry', 'Fridge'],
            'Dairy': ['Fridge'],
            'Meat': ['Fridge', 'Freezer'],
            'Beverages': ['Fridge']
        }
        
        # Units mapping
        units = {
            'Fruits': 'pieces',
            'Vegetables': 'pieces',
            'Dairy': 'liters',
            'Meat': 'kilograms',
            'Beverages': 'liters'
        }
        
        # Seed products
        for user in users:
            for category, products in category_product_map.items():
                # Choose a product from the category
                product_name = choice(products)
                
                # Choose a suitable storage place for the category
                storage_place = choice(category_storage_map[category])
                
                # Generate a random quantity and unit for the product
                quantity = randint(1, 10)
                low_limit = randint(1, 2)
                unit = units.get(category, 'unit')
                
                product = Product(
                    name=product_name,
                    category=category,
                    storage_place=storage_place,
                    quantity=quantity,
                    unit=unit,
                    low_limit = low_limit,
                    user_id=user.id
                )
                db.session.add(product)

        db.session.commit()

        print("Seed completed!")
