# Generated by Django 3.0.3 on 2020-02-28 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinefoods', '0011_auto_20200228_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carts',
            name='qty',
            field=models.IntegerField(default=1),
        ),
    ]