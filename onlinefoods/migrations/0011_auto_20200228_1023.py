# Generated by Django 3.0.3 on 2020-02-28 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlinefoods', '0010_coupons'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='cart',
            new_name='carts',
        ),
    ]