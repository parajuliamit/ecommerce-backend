from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField()
    unit = models.CharField(max_length=10)
    category = models.CharField(max_length=100,choices=[('Fruits','Fruits'),('Vegetables','Vegetables'),('Dairy','Dairy'),('Meat','Meat'),('Others','Others')])

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    shipping_address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=10)
    date_ordered = models.DateTimeField(auto_now_add=True)
    payment_status = models.BooleanField()
    payment_method = models.CharField(max_length=30)
    status = models.CharField(max_length=100,choices=[('Pending','Pending'),('Processing','Processing'),('Delivered','Delivered'),('Cancelled','Cancelled')])

    def __str__(self):
        return f"{self.user.username}'s Order {self.id}".format(self=self)

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"