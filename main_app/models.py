from django.db import models
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from datetime import date
from django.dispatch import receiver
from django.urls import reverse
from django.db.models.signals import post_save

CATEGORIES = (
  ('0', 'Snacks'),
  ('1', 'Frozen Food'),
  ('2', 'Desserts'),
  ('3', 'Beverages'),
  ('4', 'Alcohol'),
)

# Extension of built in User

class Item(models.Model):
  title = models.CharField(max_length=100)
  votes = models.IntegerField(default=1)
  status = models.BooleanField(default=False)
  amazon_id = models.CharField(max_length=100, default='')
  image_url = models.CharField(max_length=200, default='')
  categories = models.CharField(
    max_length=1,
    choices=CATEGORIES,
    default=CATEGORIES[0][0]
  )
  zipcodes = ArrayField(
    models.CharField(
      max_length=5,
    )
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title

class Vote(models.Model):
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  

class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  text = models.CharField(max_length=250)

  def __str__(self):
    return f'User: {self.user_id}, text: {self.text}'

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  favorite_item = models.ForeignKey(
    Item, 
    on_delete=models.CASCADE,
    blank=True,
    null=True
  )

  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
    if created:
      Profile.objects.create(user=instance)

  @receiver(post_save, sender=User)
  def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
  
  def __str__(self):
    return f'User: {self.user_id}, Favorite: {self.favorite_item}'

