# from django.db.models.signals import post_save
# from django.db import models
# from django.contrib.auth.models import User
# from django.dispatch import receiver
#
# # use this however u need it
# # you also need to configure the apps.py file and settings.py
# # there are many kinds of signals and multiple ways to implement them
#
#
# # you would actually store this in the models file and import it into this file
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#     first_name = models.CharField(max_length=200, null=True, blank=True)
#     last_name = models.CharField(max_length=200, null=True, blank=True)
#     phone = models.CharField(max_length=200, null=True, blank=True)
#
#     def __str__(self):
#         return str(self.first_name)
#
#
# @receiver(post_save, sender=User) # first way to do it
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# # second way to do it; after it's saved, trigger this function
# post_save.connect(create_profile, sender=User)
#
#
# @receiver(post_save, sender=User)
# def update_profile(sender, instance, created, **kwargs):
#     if not created:
#         instance.profile.save()
#
#
# post_save.connect(update_profile, sender=User)
