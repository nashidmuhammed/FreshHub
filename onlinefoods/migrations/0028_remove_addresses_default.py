# Generated by Django 3.0.3 on 2020-03-04 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlinefoods', '0027_addresses_default'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addresses',
            name='default',
        ),
    ]
