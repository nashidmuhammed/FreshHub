# Generated by Django 3.0.3 on 2020-03-05 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinefoods', '0041_remove_order_total_orderid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_total',
            name='name',
            field=models.CharField(default=123, max_length=100),
            preserve_default=False,
        ),
    ]
