# Generated by Django 2.2.4 on 2019-12-15 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0005_sporttype_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='level',
            field=models.CharField(choices=[('BEGINNER', 'Beginner'), ('ADVANCED', 'Advanced'), ('EXPERT', 'Expert')], default=1, max_length=1),
        ),
    ]
