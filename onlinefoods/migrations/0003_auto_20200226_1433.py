# Generated by Django 3.0.3 on 2020-02-26 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('onlinefoods', '0002_register'),
    ]

    operations = [
        migrations.RenameField(
            model_name='register',
            old_name='name',
            new_name='username',
        ),
    ]
