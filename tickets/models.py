from django.db import models
from django.contrib.auth.models import User
import uuid

class Ticket(models.Model):
    # Unique ID for the ticket (prevents guessing)
    ticket_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    
    # Track who created this ticket
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Track if the ticket has been used
    is_used = models.BooleanField(default=False)
    
    # Timestamp for when it was scanned (audit trail)
    scanned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.ticket_id} - {'USED' if self.is_used else 'FRESH'}"