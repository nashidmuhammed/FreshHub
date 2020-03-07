from django.db import models


class otp(models.Model):
    otp = models.CharField(max_length=6,default=123456)


class users(models.Model):
    username = models.CharField(max_length=100,unique=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100,unique=True)
    phone = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class category(models.Model):
    cname = models.CharField(max_length=100)
    cimage = models.ImageField(null=True)


class product(models.Model):
    pname = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    pimage = models.ImageField(null=True)
    price = models.FloatField()
    desc = models.TextField()
    rating = models.IntegerField(default=0)


class carts(models.Model):
    user = models.CharField(max_length=100)
    pname = models.CharField(max_length=100)
    pimage = models.ImageField(null=True)
    qty = models.IntegerField(default=1)
    price = models.FloatField()


class total(models.Model):
    user = models.CharField(max_length=100)
    subtotal = models.FloatField(default=0)
    delivery = models.FloatField(default=0)
    discount  = models.FloatField(default=0)
    totals = models.FloatField(default=0)
    counts = models.IntegerField(default=0)


class coupons(models.Model):
    code = models.CharField(max_length=100)
    amount = models.FloatField()


class wishlists(models.Model):
    user = models.CharField(max_length=100,default=0)
    wish_pid = models.IntegerField()
    wish_pname = models.CharField(max_length=100)

class addresses(models.Model):
    user = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    streetaddress = models.CharField(max_length=100)
    appartment = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100)
    zip = models.IntegerField()
    phone = models.IntegerField()
    email = models.CharField(max_length=100,null=True)
    default = models.CharField(max_length=10,null=True)

class admins(models.Model):
    admin_id = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class orders(models.Model):
    user = models.CharField(max_length=100)
    orderid = models.CharField(max_length=100)
    pname = models.CharField(max_length=100)
    pimage = models.ImageField(null=True)
    qty = models.IntegerField()
    price = models.FloatField()

class order_total(models.Model):
    user = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    subtotal = models.FloatField()
    delivery = models.FloatField()
    discount = models.FloatField(default=0)
    total = models.FloatField()
    counts = models.IntegerField()
    phone = models.IntegerField()
    address = models.CharField(max_length=200)
    appartment = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100)
    zip = models.IntegerField()
    email = models.CharField(max_length=100, null=True)



