#!/usr/bin/env python3

# Standard library imports
from random import randint, choice
from faker import Faker
from datetime import date, timedelta

# Local imports
from app import app, db  # Import Flask app and db instance
from models import User, Product, ProductItem  # Import User, Product, and ProductItem models

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
        for _ in range(2):
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
        products = []
        for user in users:
            for category, products_list in category_product_map.items():
                # Choose a product from the category
                product_name = choice(products_list)
                
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
                    low_limit=low_limit,
                    user_id=user.id
                )
                db.session.add(product)
                products.append(product)

        db.session.commit()

        # Seed product items and ensure quantity matches
        for product in products:
            # Calculate the total quantity needed
            total_quantity = product.quantity
            product_items_count = randint(1, 5)  # Ensure at least one product item

            total_product_items_quantity = 0
            for _ in range(product_items_count):
                brand_name = fake.company()
                quantity = randint(1, 5)
                expiry_date = fake.date_between(start_date="today", end_date="+1y")
                
                # Accumulate the quantity of product items
                total_product_items_quantity += quantity

                product_item = ProductItem(
                    product_id=product.id,
                    brand_name=brand_name,
                    quantity=quantity,
                    expiry_date=expiry_date
                )
                db.session.add(product_item)

            # Update the product quantity to match the total quantity of product items
            product.quantity = total_product_items_quantity

        db.session.commit()

        print("Seed completed!")
