# Generated by Django 3.0.3 on 2020-02-27 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinefoods', '0007_auto_20200227_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='pimage',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
