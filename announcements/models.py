from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class House(models.Model):
    description = models.CharField(max_length=600)
    contact_email = models.EmailField()

class Announcement(models.Model):
    pub_date = models.DateTimeField('date published')
    title = models.CharField(max_length=255)
    number_of_bets = models.IntegerField(default=0, editable=False)
    house = models.OneToOneField(House, on_delete=models.CASCADE)
    auction_completed = models.BooleanField(default=False)
    max_bet = models.IntegerField(default=0)
    bet_to_complete = models.IntegerField(default=1000)
    sold_to = models.CharField(max_length=255, blank=True, null=True, editable=False)

class Photo(models.Model):
    src = models.ImageField(blank=True, null=True, upload_to="images/")
    house = models.ForeignKey(House, on_delete=models.CASCADE, blank=True, null=True, )

class Message(models.Model):
    chat = models.ForeignKey(Announcement, verbose_name='Chat under announcement', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    message = models.TextField('Message')
    pub_date = models.DateTimeField('Message Date', default=timezone.now)
