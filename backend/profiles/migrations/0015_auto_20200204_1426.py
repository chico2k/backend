# Generated by Django 2.2.8 on 2020-02-04 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0014_auto_20200204_1304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='review',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='sport',
        ),
    ]
