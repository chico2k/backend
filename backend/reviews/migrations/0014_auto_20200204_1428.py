# Generated by Django 2.2.8 on 2020-02-04 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0013_auto_20200204_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review', to='profiles.Profile'),
        ),
    ]
