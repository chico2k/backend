# Generated by Django 2.2.4 on 2019-12-20 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20191118_2057'),
        ('reviews', '0002_auto_20191220_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_author',
            field=models.OneToOneField(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='review_author', to='profiles.Profile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='review_profile', to='profiles.Profile'),
        ),
    ]
