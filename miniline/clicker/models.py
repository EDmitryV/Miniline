import os.path

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from copy import copy
from .constants import *
from django.conf import settings


def load_default_words_set(lang_code):
    try:
        return WordsSet.objects.get(lang_code=lang_code)
    except:
        path = os.path.dirname(os.path.realpath(__file__)).replace('clicker', 'words_sets') + "/{}.txt".format(
            lang_code)
        with open(path, "r", encoding='UTF-8') as f:
            return WordsSet.objects.create(lang_code=lang_code, content=f.read())


class WordsSet(models.Model):
    lang_code = models.TextField(null=False)
    content = models.TextField(null=False)


class GameCore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    click_power = models.IntegerField(default=1)
    auto_click_power = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    night_theme = models.BooleanField(default=False)
    lang_code = models.TextField(default='en')
    words_set = models.ForeignKey(WordsSet, on_delete=models.SET_NULL, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            print("user created")
            GameCore.objects.create(user=instance, words_set=load_default_words_set(lang_code="en"))

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
        return (self.level ** 2) * 20 * (self.level)

    def set_language(self, lang_code):
        for lang_pare in settings.LANGUAGES:
            if lang_pare[0] == lang_code:
                self.lang_code = lang_code
                break

    def set_words_set(self, lang_code, content=""):
        print("update words set: " + lang_code)
        if self.words_set.lang_code == "my":
            self.words_set.delete()
        contains = False
        for lang_pare in settings.LANGUAGES:
            if lang_pare[0] == lang_code:
                contains = True
                break
        if lang_code == "my" or not contains:
            if not content:
                self.words_set = load_default_words_set(lang_code=lang_code)
            else:
                self.words_set = WordsSet.objects.create(lang_code=lang_code, content=content)
        else:
            self.words_set = load_default_words_set(lang_code=lang_code)


class Boost(models.Model):
    core = models.ForeignKey(GameCore, null=False, on_delete=models.CASCADE)
    power = models.IntegerField(default=1)
    level = models.IntegerField(default=0)
    price = models.IntegerField(default=10)
    type = models.PositiveSmallIntegerField(
        default=0, choices=BOOST_TYPE_CHOICES)

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
