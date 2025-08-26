#!/usr/bin/env python3
"""
MongoDB Connection Verification Script
For employers to verify database access and credentials
"""

from pymongo import MongoClient
import sys

# Connection credentials
HOST = "localhost"
PORT = 27017
DB_NAME = "kasa_reservations"
COLLECTION_NAME = "reservations"
USERNAME = "kasa_admin"
PASSWORD = "KasaChallenge2025!"

def verify_connection():
    """Verify MongoDB connection and display sample data"""
    try:
        print("=== MongoDB Connection Verification ===\n")
        
        # Connect to MongoDB
        connection_string = f"mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
        print(f"Connecting to: {connection_string}")
        
        client = MongoClient(connection_string)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        # Test connection
        db.command('ping')
        print("✅ Connection successful!")
        
        # Get document count
        count = collection.count_documents({})
        print(f"✅ Found {count} documents in collection '{COLLECTION_NAME}'")
        
        # Display sample document
        sample_doc = collection.find_one()
        if sample_doc:
            print("\n📄 Sample document structure:")
            for key, value in sample_doc.items():
                if key != '_id':
                    print(f"   {key}: {type(value).__name__}")
        
        # Run aggregation pipeline
        print("\n🔍 Running aggregation pipeline...")
        pipeline = [
            {
                "$project": {
                    "_id": 0,
                    "building_city": "$building",
                    "confirmation_code": "$reservation_code",
                    "checkin_date": "$ds_checkin",
                    "booking_platform": "$booking_platform"
                }
            },
            {"$limit": 5}
        ]
        
        results = list(collection.aggregate(pipeline))
        print(f"\n📊 Aggregation Results (first 5 documents):")
        print("-" * 60)
        print(f"{'Building/City':<20} {'Confirmation Code':<15} {'Platform':<10}")
        print("-" * 60)
        
        for result in results:
            city = str(result.get('building_city', 'N/A'))
            code = str(result.get('confirmation_code', 'N/A'))
            platform = str(result.get('booking_platform', 'N/A'))
            print(f"{city:<20} {code:<15} {platform:<10}")
        
        print("\n✅ All verification tests passed!")
        print("✅ Database is ready for employer review!")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = verify_connection()
    sys.exit(0 if success else 1)
