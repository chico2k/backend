# Generated by Django 2.2.8 on 2020-03-25 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_auto_20200324_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='profiles.Profile'),
        ),
    ]
