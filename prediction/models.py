from django.db import models

# Create a dummy model (even if not used)
class Dummy(models.Model):
    name = models.CharField(max_length=100)
