# Generated by Django 2.2.4 on 2019-12-26 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_auto_20191220_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='average_rating',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=3),
        ),
    ]
