from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    # CASCADE will delete the relationship to the customer upon user deletion
    # User class will hold registered users
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='shitass.png', null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True) # null=True allows it to be empty
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self): # shows name variable in admin panel
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door'),
    )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)  # allows for multiple selections

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )

    # when a customer is deleted the customer value will be set to null; gives dropdown menu of customers
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.product.name
