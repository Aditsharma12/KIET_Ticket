"""
Test script to verify MongoDB connection.
Run this to ensure the MongoDB connection is working properly.
"""

import os
import sys
import django

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'entry_system.settings')
django.setup()

from tickets.mongodb_utils import get_mongo_client, get_mongo_db, get_tickets_collection

def test_connection():
    """Test MongoDB connection"""
    try:
        print("Testing MongoDB connection...")
        
        # Test client connection
        client = get_mongo_client()
        print("[OK] Successfully created MongoDB client")
        
        # Test database connection
        db = get_mongo_db()
        print(f"[OK] Successfully connected to database: {db.name}")
        
        # Test collection access
        tickets_collection = get_tickets_collection()
        print(f"[OK] Successfully accessed tickets collection")
        
        # Test ping
        client.admin.command('ping')
        print("[OK] Successfully pinged MongoDB server")
        
        # Show existing collections
        collections = db.list_collection_names()
        print(f"\nExisting collections in database: {collections}")
        
        # Count tickets
        ticket_count = tickets_collection.count_documents({})
        print(f"Number of tickets in collection: {ticket_count}")
        
        print("\n[SUCCESS] MongoDB connection is working perfectly!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error connecting to MongoDB: {e}")
        return False

if __name__ == "__main__":
    test_connection()
