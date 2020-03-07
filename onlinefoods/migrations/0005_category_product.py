# Generated by Django 3.0.3 on 2020-02-26 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinefoods', '0004_auto_20200226_1437'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cname', models.CharField(max_length=100)),
                ('cimage', models.ImageField(null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('pimage', models.ImageField(null=True, upload_to='')),
                ('price', models.FloatField()),
                ('desc', models.TextField()),
                ('rating', models.IntegerField(default=0)),
            ],
        ),
    ]