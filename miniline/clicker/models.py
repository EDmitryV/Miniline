from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Connection(models.Model):
    creator = models.ForeignKey(User, related_name='creator')
    opponent = models.ForeignKey(User, related_name='opponent', null=true, blank=true)

class CurrentGameCore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    click_power = models.IntegerField(default=1)
    auto_click_power = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

class Buster(models.Model):
    core = ForeignKey(CurrentGameCore, related_name='core')
    power = IntegerField(default=0)
    level = IntegerField(default=0)
    upgrade_power = IntegerField(blank=False, null=False)