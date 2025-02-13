from django.db import models

# Create your models here.

class Holiday(models.Model):
    name=models.CharField(max_length=255)
    description=models.TextField(blank=True, null=True)
    date=models.DateField()
    country_code=models.CharField(max_length=2)
    holiday_type=models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name