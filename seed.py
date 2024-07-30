#!/usr/bin/env python3

# Standard library imports
from random import randint
from faker import Faker

# Local imports
from app import app, db  # Import Flask app and db instance
from models import User

if __name__ == '__main__':
    fake = Faker()
    
    # Initialize Flask app context
    with app.app_context():
        print("Starting seed...")
        
        # Clear existing data (optional)
        db.drop_all()
        db.create_all()
        
        # Seed code

        for _ in range(4):
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                picture="https://picsum.photos/983/458" # Add a fake picture URL for each user
            )
            db.session.add(user)

        dan = User(username='dan',
                email='danspmunene@gmail.com',
                password="munene",
                picture="https://picsum.photos/983/458" # Add a fake picture URL for each user 
                )
        db.session.add(dan)

        db.session.commit()

        print("Seed completed!")