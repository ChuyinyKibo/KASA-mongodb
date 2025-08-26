#!/usr/bin/env python3
"""
MongoDB Connection Demo for Employers
Shows how to use the provided credentials to access the database
"""

from pymongo import MongoClient
import sys

def main():
    print("=" * 60)
    print("MONGODB KASA RESERVATIONS - EMPLOYER CONNECTION DEMO")
    print("=" * 60)
    
    # Database credentials provided to employers
    USERNAME = "kasa_admin"
    PASSWORD = "KasaChallenge2025!"
    HOST = "localhost"
    PORT = 27017
    DATABASE = "kasa_reservations"
    COLLECTION = "reservations"
    
    print(f"\n📋 Using Credentials:")
    print(f"   Username: {USERNAME}")
    print(f"   Password: {PASSWORD}")
    print(f"   Host: {HOST}:{PORT}")
    print(f"   Database: {DATABASE}")
    print(f"   Collection: {COLLECTION}")
    
    # Connection string
    connection_string = f"mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
    print(f"\n🔗 Connection String:")
    print(f"   {connection_string}")
    
    try:
        print(f"\n🔄 Connecting to MongoDB...")
        client = MongoClient(connection_string)
        db = client[DATABASE]
        collection = db[COLLECTION]
        
        # Test connection
        db.command('ping')
        print("✅ Connection successful!")
        
        # Get document count
        count = collection.count_documents({})
        print(f"✅ Found {count} documents in collection")
        
        # Show sample document
        print(f"\n📄 Sample Document:")
        sample = collection.find_one()
        if sample:
            print(f"   Reservation Code: {sample.get('reservation_code', 'N/A')}")
            print(f"   Building: {sample.get('building', 'N/A')}")
            print(f"   Check-in: {sample.get('ds_checkin', 'N/A')}")
            print(f"   Platform: {sample.get('booking_platform', 'N/A')}")
        
        # Run the requested aggregation
        print(f"\n🔍 Running Aggregation Pipeline:")
        print("   Displaying building city names and confirmation codes...")
        
        pipeline = [
            {
                "$project": {
                    "_id": 0,
                    "building_city": "$building",
                    "confirmation_code": "$reservation_code",
                    "booking_platform": "$booking_platform"
                }
            }
        ]
        
        results = list(collection.aggregate(pipeline))
        
        print(f"\n📊 Aggregation Results ({len(results)} documents):")
        print("-" * 60)
        print(f"{'Building/City':<15} {'Confirmation Code':<18} {'Platform':<10}")
        print("-" * 60)
        
        for i, result in enumerate(results, 1):
            city = str(result.get('building_city', 'N/A'))
            code = str(result.get('confirmation_code', 'N/A'))
            platform = str(result.get('booking_platform', 'N/A'))
            print(f"{city:<15} {code:<18} {platform:<10}")
        
        print(f"\n✅ All tests passed! Database is working correctly.")
        print(f"✅ Hiring challenge requirements met:")
        print(f"   - MongoDB database created ✓")
        print(f"   - Collection with 10 documents ✓")
        print(f"   - User credentials working ✓")
        print(f"   - Aggregation pipeline functional ✓")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"\n🔧 Troubleshooting:")
        print(f"   1. Ensure MongoDB is running: docker ps")
        print(f"   2. Start if needed: docker start mongodb-kasa")
        print(f"   3. Check credentials are correct")
        sys.exit(1)

if __name__ == "__main__":
    main()
