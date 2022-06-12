from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from copy import copy
from .constants import *


class WordsSet(models.Model):
    lang = models.TextField(default="")
    words = models.TextField(default="")


class GameCore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    click_power = models.IntegerField(default=1)
    auto_click_power = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    words_set = models.ForeignKey(WordsSet, null=True, on_delete=models.SET_DEFAULT, default=1)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            GameCore.objects.create(user=instance)

    def set_points(self, points, commit=True):
        self.points = points
        is_levelupdated = self.is_levelup()
        boost_type = self.get_boost_type()

        if is_levelupdated:
            self.level += 1

        if commit:
            self.save()

        return is_levelupdated, boost_type


    def is_levelup(self):
        return self.points >= self.calculate_next_level_price()


    def get_boost_type(self):
        boost_type = 0
        if self.level % 3 == 0:
            boost_type = 1
        return boost_type


    def calculate_next_level_price(self):
        return (self.level ** 2) * 10 * (self.level)

class Boost(models.Model):
    core = models.ForeignKey(GameCore, null=False, on_delete=models.CASCADE)
    power = models.IntegerField(default=1)
    level = models.IntegerField(default=0)
    price = models.IntegerField(default=10)
    type = models.PositiveSmallIntegerField(default=0, choices=BOOST_TYPE_CHOICES)

    def levelup(self, current_points):
        if self.price > current_points:
            return False

        old_boost_stats = copy(self)

        self.core.points = current_points - self.price

        self.core.click_power += self.power * BOOST_TYPE_VALUES[self.type][
            'click_power_scale']
        self.core.auto_click_power += self.power * BOOST_TYPE_VALUES[self.type][
            'auto_click_power_scale']
        self.core.save()

        self.level += 1
        self.power *= 2
        self.price *= BOOST_TYPE_VALUES[self.type]['price_scale']
        self.save()

        return old_boost_stats, self