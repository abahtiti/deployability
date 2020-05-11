from django.db import models
from django.contrib.auth.models import User


class Blocker(models.Model):
    # title (ex: iad6-71)
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Campaigns(models.Model):
    # title (ex: iad6-71)
    devices = models.TextField()
    def __str__(self):
        return self.devices
    #CHOICES=[('select1','select 1'),('select2','select 2')]
    #like = models.ChoiceField(choices=CHOICES, widget=models.RadioSelect)

    # pub_date
    # ETA
    # body
