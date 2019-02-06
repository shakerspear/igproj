from django.db import models

#counsolers
class counsoler(models.Model):
    name = models.CharField(max_length=64)
    salary = models.IntegerField()
    guaranteed = models.IntegerField()
    total = models.IntegerField()
#students

#packages
