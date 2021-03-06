from django.db import models
from django.contrib.auth.models import User


class CheckIn(models.Model):
    date = models.DateField()
    notes = models.TextField(blank=True)
    place = models.ForeignKey('Place')

    def __str__(self):
        return self.place + ' on ' + str(self.date_and_time)


class Place(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    notes = models.TextField(blank=True)
    place_id = models.CharField(max_length=100, null=True) # for google places api, may not be necessary
    togo = models.BooleanField(default=False)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name

