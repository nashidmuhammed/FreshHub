# Generated by Django 3.0.3 on 2020-03-06 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinefoods', '0043_auto_20200306_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]