from django.contrib import admin

# Register your models here.
from onlinefoods.models import otp,users,product,category,carts,coupons,total,wishlists,addresses,orders,order_total,admins
admin.site.register(otp)
admin.site.register(users)
admin.site.register(category)
admin.site.register(product)
admin.site.register(carts)
admin.site.register(coupons)
admin.site.register(total)
admin.site.register(wishlists)
admin.site.register(addresses)
admin.site.register(orders)
admin.site.register(order_total)
admin.site.register(admins)