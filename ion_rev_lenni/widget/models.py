# models.py
from django.db import models


class Test(models.Model):
    lead_time = models.DurationField()