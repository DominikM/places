from django.db import models


class CheckIn(models.Model):
    date_and_time = models.DateTimeField()
    notes = models.TextField()
    place = models.ForeignKey('Place')

    def __str__(self):
        return self.place + ' on ' + str(self.date_and_time)


class Place(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    lat = models.DecimalField(max_digits=8, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    notes = models.TextField()

    def __str__(self):
        return self.name

