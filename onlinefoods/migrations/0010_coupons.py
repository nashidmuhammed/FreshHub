# Generated by Django 3.0.3 on 2020-02-27 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinefoods', '0009_auto_20200227_1510'),
    ]

    operations = [
        migrations.CreateModel(
            name='coupons',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100)),
                ('amount', models.FloatField()),
            ],
        ),
    ]