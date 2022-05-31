from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Session(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    click_power = models.FloatField(default=1.0)
    auto_click_power = models.FloatField(default=0.0)
    start_time = models.DateTimeField()
    status = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_user_session(sender, instance, created, **kwargs):
        if created:
            Session.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_session(sender, instance, **kwargs):
        instance.progress.save()
