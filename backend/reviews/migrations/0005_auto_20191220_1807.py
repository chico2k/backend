# Generated by Django 2.2.4 on 2019-12-20 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20191118_2057'),
        ('reviews', '0004_auto_20191220_1805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='profile',
        ),
        migrations.AddField(
            model_name='review',
            name='profile',
            field=models.ForeignKey(default='2', on_delete=django.db.models.deletion.CASCADE, related_name='review_profile', to='profiles.Profile'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='review',
            name='review_author',
        ),
        migrations.AddField(
            model_name='review',
            name='review_author',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='review_author', to='profiles.Profile'),
            preserve_default=False,
        ),
    ]
