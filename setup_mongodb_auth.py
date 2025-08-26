#!/usr/bin/env python3
"""
MongoDB Setup Script with Authentication for Kasa Reservations
Creates authenticated MongoDB database with proper user credentials
"""

import pandas as pd
import pymongo
from pymongo import MongoClient
import os
from datetime import datetime
import json
import time

# Database configuration
DB_NAME = "kasa_reservations"
COLLECTION_NAME = "reservations"
DB_USERNAME = "kasa_admin"
DB_PASSWORD = "KasaChallenge2025!"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "AdminPass2025!"
HOST = "localhost"
PORT = 27017

def wait_for_mongodb():
    """Wait for MongoDB to be ready"""
    print("Waiting for MongoDB to start...")
    for i in range(30):
        try:
            client = MongoClient(f'mongodb://{ADMIN_USERNAME}:{ADMIN_PASSWORD}@{HOST}:{PORT}/admin')
            client.admin.command('ping')
            print("MongoDB is ready!")
            client.close()
            return True
        except Exception as e:
            print(f"Attempt {i+1}: MongoDB not ready yet...")
            time.sleep(2)
    return False

def load_excel_data(file_path):
    """Load and parse reservation data from Excel file"""
    try:
        df = pd.read_excel(file_path)
        print(f"Loaded Excel file with {len(df)} rows and columns: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"Error loading Excel file: {e}")
        return None

def create_database_user():
    """Create database user with proper permissions"""
    try:
        # Connect as admin
        admin_client = MongoClient(f'mongodb://{ADMIN_USERNAME}:{ADMIN_PASSWORD}@{HOST}:{PORT}/admin')
        
        # Switch to the target database
        db = admin_client[DB_NAME]
        
        # Create user with readWrite permissions on the database
        db.command("createUser", DB_USERNAME,
                  pwd=DB_PASSWORD,
                  roles=[{"role": "readWrite", "db": DB_NAME}])
        
        print(f"Created database user: {DB_USERNAME}")
        admin_client.close()
        return True
        
    except pymongo.errors.DuplicateKeyError:
        print(f"User {DB_USERNAME} already exists")
        return True
    except Exception as e:
        print(f"Error creating database user: {e}")
        return False

def setup_authenticated_database():
    """Setup MongoDB database with authentication"""
    try:
        # Connect with database user credentials
        client = MongoClient(f'mongodb://{DB_USERNAME}:{DB_PASSWORD}@{HOST}:{PORT}/{DB_NAME}')
        
        # Create database and collection
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        # Test the connection
        db.command('ping')
        
        print(f"Connected to authenticated MongoDB database: {DB_NAME}")
        print(f"Created collection: {COLLECTION_NAME}")
        
        return client, db, collection
        
    except Exception as e:
        print(f"Error setting up authenticated database: {e}")
        return None, None, None

def transform_reservation_data(df):
    """Transform Excel data into MongoDB documents"""
    documents = []
    
    for index, row in df.iterrows():
        doc = {}
        
        # Map Excel columns to document fields
        for col in df.columns:
            value = row[col]
            field_name = col.lower().replace(' ', '_').replace('-', '_')
            
            if pd.isna(value):
                doc[field_name] = None
            elif isinstance(value, (pd.Timestamp, datetime)):
                doc[field_name] = value
            else:
                doc[field_name] = value
        
        # Add metadata
        doc['_created_at'] = datetime.now()
        doc['_document_id'] = index + 1
        
        documents.append(doc)
    
    return documents[:10]  # Return only first 10 as requested

def insert_reservations(collection, documents):
    """Insert reservation documents into MongoDB"""
    try:
        result = collection.insert_many(documents)
        print(f"Inserted {len(result.inserted_ids)} reservation documents")
        return result.inserted_ids
    except Exception as e:
        print(f"Error inserting documents: {e}")
        return []

def create_aggregation_pipeline(collection):
    """Create aggregation to display building city and confirmation code"""
    
    pipeline = [
        {
            "$project": {
                "_id": 0,
                "building_city": "$building",
                "confirmation_code": "$reservation_code",
                "checkin_date": "$ds_checkin",
                "checkout_date": "$ds_checkout",
                "overall_rating": "$overall_rating",
                "booking_platform": "$booking_platform"
            }
        }
    ]
    
    print("\nExecuting aggregation pipeline...")
    results = list(collection.aggregate(pipeline))
    
    print(f"\nAggregation Results ({len(results)} documents):")
    print("-" * 70)
    print(f"{'#':<3} {'Building/City':<25} {'Confirmation Code':<20} {'Platform':<10}")
    print("-" * 70)
    
    for i, result in enumerate(results, 1):
        city = result.get('building_city', 'N/A')
        code = result.get('confirmation_code', 'N/A')
        platform = result.get('booking_platform', 'N/A')
        print(f"{i:<3} {str(city):<25} {str(code):<20} {str(platform):<10}")
    
    return results

def test_connection():
    """Test connection with credentials"""
    try:
        client = MongoClient(f'mongodb://{DB_USERNAME}:{DB_PASSWORD}@{HOST}:{PORT}/{DB_NAME}')
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        # Test query
        count = collection.count_documents({})
        print(f"Connection test successful! Found {count} documents in collection.")
        
        client.close()
        return True
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False

def main():
    """Main execution function"""
    print("=== MongoDB Kasa Reservations Setup with Authentication ===\n")
    
    # Wait for MongoDB to be ready
    if not wait_for_mongodb():
        print("MongoDB failed to start. Exiting.")
        return
    
    # Create database user
    if not create_database_user():
        print("Failed to create database user. Exiting.")
        return
    
    # Load Excel data
    excel_file = "reservations.xlsx"
    df = load_excel_data(excel_file)
    
    if df is None:
        print("Failed to load Excel data. Exiting.")
        return
    
    # Setup authenticated database
    client, db, collection = setup_authenticated_database()
    
    if collection is None:
        print("Failed to setup authenticated database. Exiting.")
        return
    
    # Clear existing data
    collection.delete_many({})
    print("Cleared existing collection data")
    
    # Transform and insert data
    documents = transform_reservation_data(df)
    print(f"\nTransformed {len(documents)} documents")
    
    inserted_ids = insert_reservations(collection, documents)
    
    if inserted_ids:
        print(f"\nSuccessfully inserted {len(inserted_ids)} reservations")
        
        # Create and execute aggregation
        aggregation_results = create_aggregation_pipeline(collection)
        
        # Test connection
        print("\n" + "="*60)
        print("TESTING CONNECTION WITH CREDENTIALS")
        print("="*60)
        client.close()  # Close current connection
        test_connection()
        
        # Print connection details
        print("\n" + "="*60)
        print("DATABASE CONNECTION CREDENTIALS FOR EMPLOYERS")
        print("="*60)
        print(f"Host: {HOST}")
        print(f"Port: {PORT}")
        print(f"Database: {DB_NAME}")
        print(f"Collection: {COLLECTION_NAME}")
        print(f"Username: {DB_USERNAME}")
        print(f"Password: {DB_PASSWORD}")
        print(f"Connection String: mongodb://{DB_USERNAME}:{DB_PASSWORD}@{HOST}:{PORT}/{DB_NAME}")
        print("\nAdmin Credentials (for full access):")
        print(f"Admin Username: {ADMIN_USERNAME}")
        print(f"Admin Password: {ADMIN_PASSWORD}")
        print(f"Admin Connection: mongodb://{ADMIN_USERNAME}:{ADMIN_PASSWORD}@{HOST}:{PORT}/admin")
        print("="*60)
        print("\nMongoDB is now running with authentication enabled!")
        print("Employers can connect using the credentials above.")
    
    else:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    main()
