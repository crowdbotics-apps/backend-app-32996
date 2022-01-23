from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator
import re
from home.constants import *
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


# class UserDetails(models.Model):
#     id = models.AutoField(primary_key=True)
#     username = models.CharField(max_length=150, blank=False, validators=[
#         RegexValidator(
#             regex='^[\w.@+-]+$',
#             message="Letters, digits and @/./+/-/_ only",
#             flags=re.IGNORECASE,
#         )])
#     email = models.EmailField(blank=False)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=150)


class App(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(
        max_length=6,
        choices=APP_CHOICES
    )
    framework = models.CharField(
        max_length=12,
        choices=FRAMEWORK_CHOICES
    )
    domain_name = models.CharField(max_length=50, null=True, blank=True)
    screenshot = models.TextField(null=True)
    subscription = models.ForeignKey('Subscription', related_name='+', on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField('%m/%d/%Y %H:%M:%S', auto_now_add=True)
    updated_at = models.DateTimeField('%m/%d/%Y %H:%M:%S', auto_now=True)

class Plan(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=False)
    description = models.TextField(blank=False)
    price = models.CharField(
        max_length=7,
        choices=PRICE_CHOICES,
        default=PRICE_CHOICES_LIST[0],
        blank=False
    )
    created_at = models.DateTimeField('%m/%d/%Y %H:%M:%S', default=timezone.now(), editable=False)
    updated_at = models.DateTimeField('%m/%d/%Y %H:%M:%S', default=timezone.now(), editable=False)


class Subscription(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    app = models.ForeignKey(App, related_name='+', on_delete=models.CASCADE)
    active = models.BooleanField(blank=False)
    created_at = models.DateTimeField('%m/%d/%Y %H:%M:%S', auto_now_add=True)
    updated_at = models.DateTimeField('%m/%d/%Y %H:%M:%S', auto_now=True)

    def save(self, *arg, **kwargs):
        Subscription.objects.filter(app=self.app_id).update(active=False)
        super(Subscription, self).save(*arg, **kwargs)
        self.app.subscription_id = self.id
        self.app.save()
