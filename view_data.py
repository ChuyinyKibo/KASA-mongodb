#!/usr/bin/env python3
"""
MongoDB Data Viewer - Display all reservation data
"""

from pymongo import MongoClient
import json
from datetime import datetime

# Connection credentials
HOST = "localhost"
PORT = 27017
DB_NAME = "kasa_reservations"
COLLECTION_NAME = "reservations"
USERNAME = "kasa_admin"
PASSWORD = "KasaChallenge2025!"

def view_all_data():
    """Display all reservation data in readable format"""
    try:
        # Connect to MongoDB
        client = MongoClient(f'mongodb://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}')
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        print("=== KASA RESERVATIONS DATABASE ===\n")
        
        # Get all documents
        documents = list(collection.find())
        print(f"Total Documents: {len(documents)}\n")
        
        # Display each document
        for i, doc in enumerate(documents, 1):
            print(f"📋 RESERVATION #{i}")
            print("-" * 50)
            print(f"Reservation Code: {doc.get('reservation_code', 'N/A')}")
            print(f"Building: {doc.get('building', 'N/A')}")
            print(f"Check-in: {doc.get('ds_checkin', 'N/A')}")
            print(f"Check-out: {doc.get('ds_checkout', 'N/A')}")
            print(f"Overall Rating: {doc.get('overall_rating', 'N/A')}")
            print(f"Booking Platform: {doc.get('booking_platform', 'N/A')}")
            print(f"Primary Issue: {doc.get('primary_issue', 'N/A')}")
            if doc.get('overall_comments'):
                print(f"Comments: {doc.get('overall_comments', 'N/A')}")
            print()
        
        # Show aggregation results
        print("🔍 AGGREGATION: Building City & Confirmation Codes")
        print("=" * 60)
        
        pipeline = [
            {
                "$project": {
                    "_id": 0,
                    "building_city": "$building",
                    "confirmation_code": "$reservation_code",
                    "checkin_date": "$ds_checkin",
                    "booking_platform": "$booking_platform"
                }
            }
        ]
        
        results = list(collection.aggregate(pipeline))
        print(f"{'#':<3} {'Building/City':<15} {'Confirmation Code':<18} {'Platform':<10} {'Check-in':<12}")
        print("-" * 60)
        
        for i, result in enumerate(results, 1):
            city = str(result.get('building_city', 'N/A'))
            code = str(result.get('confirmation_code', 'N/A'))
            platform = str(result.get('booking_platform', 'N/A'))
            checkin = str(result.get('checkin_date', 'N/A'))[:10] if result.get('checkin_date') else 'N/A'
            print(f"{i:<3} {city:<15} {code:<18} {platform:<10} {checkin:<12}")
        
        client.close()
        
    except Exception as e:
        print(f"Error viewing data: {e}")

if __name__ == "__main__":
    view_all_data()
