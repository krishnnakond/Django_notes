# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.



class Notes(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	note = models.TextField()
	user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True, editable=False)
	updated = models.DateTimeField(auto_now_add=True)

class Label(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255, null=True)
	note = models.ForeignKey(Notes, null=True ,related_name="notes")
	created = models.DateTimeField(auto_now_add=True, editable=False)
	updated = models.DateTimeField(auto_now_add=True)


