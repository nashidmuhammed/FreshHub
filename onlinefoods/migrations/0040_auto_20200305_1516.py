# Generated by Django 3.0.3 on 2020-03-05 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinefoods', '0039_auto_20200304_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_total',
            name='orderid',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orders',
            name='orderid',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
