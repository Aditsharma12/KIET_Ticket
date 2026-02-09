"""
MongoDB utility functions for direct MongoDB access.
This allows using MongoDB alongside Django's default database.
"""

from pymongo import MongoClient
from django.conf import settings


def get_mongo_client():
    """
    Returns a MongoDB client instance.
    """
    return MongoClient(settings.MONGODB_URI)


def get_mongo_db():
    """
    Returns the MongoDB database instance.
    """
    client = get_mongo_client()
    return client[settings.MONGODB_DB_NAME]


def get_tickets_collection():
    """
    Returns the tickets collection from MongoDB.
    """
    db = get_mongo_db()
    return db['tickets']


# Example usage:
# from tickets.mongodb_utils import get_tickets_collection
# 
# # Insert a ticket
# tickets = get_tickets_collection()
# ticket_data = {
#     'ticket_id': 'ABC123',
#     'is_used': False,
#     'scanned_at': None
# }
# tickets.insert_one(ticket_data)
#
# # Query tickets
# all_tickets = tickets.find()
# unused_tickets = tickets.find({'is_used': False})
