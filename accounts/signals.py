from django.db.models.signals import post_save
from .models import Customer
from django.contrib.auth.models import User, Group


# don't forget to config apps.py or settings.py
def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customers')
        instance.groups.add(group)
        Customer.objects.create(user=instance, name=instance.name)


# will be called when an instance of User is saved
post_save.connect(customer_profile, sender=User)
