# MongoDB Integration Guide

## Overview
Your Django project now uses **MongoDB exclusively** as its database via the djongo connector. SQLite has been completely removed.

## Configuration
- **Database Engine**: djongo
- **MongoDB URI**: `mongodb+srv://aditsharma2005vs_db_user:A1D2I3T4@ticket.9f9ssoy.mongodb.net/?appName=Ticket`
- **Database Name**: `ticket_db`

## Django Version
- **Django**: 4.1.13 (djongo compatibility requirement)
- **djongo**: 1.3.6
- **pymongo**: 3.12.3

## Usage

### Using Django ORM (Recommended)

You can now use Django's ORM normally with your models. All data is stored in MongoDB:

```python
from tickets.models import Ticket
import uuid
from datetime import datetime

# Create a ticket using Django ORM
ticket = Ticket.objects.create(
    ticket_id=str(uuid.uuid4()),
    is_used=False
)

# Query tickets
all_tickets = Ticket.objects.all()
unused_tickets = Ticket.objects.filter(is_used=False)

# Update a ticket
ticket = Ticket.objects.get(ticket_id='some-id')
ticket.is_used = True
ticket.scanned_at = datetime.now()
ticket.save()

# Delete a ticket
Ticket.objects.filter(ticket_id='some-id').delete()
```

### Using PyMongo Directly (Optional)

For advanced MongoDB operations, you can still use PyMongo:

```python
from pymongo import MongoClient

client = MongoClient('mongodb+srv://aditsharma2005vs_db_user:A1D2I3T4@ticket.9f9ssoy.mongodb.net/?appName=Ticket')
db = client['ticket_db']
tickets_collection = db['tickets_ticket']  # Django prefixes with app_model

# Direct MongoDB operations
tickets_collection.find_one({'ticket_id': 'some-id'})
```

## Migrations

Run migrations as usual:

```bash
python manage.py makemigrations
python manage.py migrate
```

All Django models (User, Session, Admin, Ticket, etc.) are now stored in MongoDB collections.

## Important Notes

1. **Django Version**: djongo requires Django 4.1.13, not Django 6.x
2. **All in MongoDB**: Everything including auth, sessions, and admin data is in MongoDB
3. **Collection Names**: Django creates collections with format `{app_name}_{model_name}` (e.g., `tickets_ticket`)
4. **No SQLite**: The `db.sqlite3` file is no longer used and can be deleted

## Database Management

### Django Admin
Create a superuser to access Django admin:
```bash
python manage.py createsuperuser
```

### MongoDB Compass
You can also connect MongoDB Compass using the connection string to view/edit data directly:
```
mongodb+srv://aditsharma2005vs_db_user:A1D2I3T4@ticket.9f9ssoy.mongodb.net/?appName=Ticket
```

## When to Use MongoDB

Use MongoDB when you need:
- More flexible schema for tickets
- Better scalability for large numbers of tickets
- Real-time updates and monitoring
- Cloud-based data storage

Use Django's SQLite/ORM when you need:
- Django's built-in features (admin, auth, sessions)
- Relational data modeling
- Django's query ORM syntax
