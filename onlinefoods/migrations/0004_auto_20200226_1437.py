# Generated by Django 3.0.3 on 2020-02-26 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlinefoods', '0003_auto_20200226_1433'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='register',
            new_name='users',
        ),
    ]
