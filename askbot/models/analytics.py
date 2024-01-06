from django.db import models
from django.contrib.auth.models import User

"""
class Dimension(models.Model):
    name = models.CharField(max_length=64, help_text="Name of the dimension")
    description = models.TextField(blank=True, null=True, help_text="Description of the dimension")
    query = models.CharField(max_length=256, help_text="Django ORM query, Python code string")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Metric(models.Model):
    name = models.CharField(max_length=64, help_text="Name of the metric")
    description = models.TextField(blank=True, null=True, help_text="Description of the metric")
    query = models.CharField(max_length=256, help_text="Django ORM query, Python code string")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
"""


class Session(models.Model):
    """Analytics session"""
    session_id = models.CharField(max_length=40, help_text="Django session ID")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Event(models.Model):
    """Analytics event"""
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, help_text="Name of the event")
    timestamp = models.DateTimeField(auto_now_add=True)
