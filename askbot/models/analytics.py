from django.db import models
from django.contrib.auth.models import User


class DimensionBlueprint(models.Model):
    name = models.CharField(max_length=64, help_text="Name of the dimension")
    description = models.TextField(blank=True, null=True, help_text="Description of the group")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Dimension(models.Model):
    name = models.CharField(max_length=64, help_text="Name of the dimension")
    description = models.TextField(blank=True, null=True, help_text="Description of the group")
    expression = models.CharField(max_length=256, help_text="Expression to be used in the query")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Session(models.Model):
    session_id = models.CharField(max_length=40, help_text="Django session ID")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=512)
    dimensions = models.ManyToManyField(Dimension, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
