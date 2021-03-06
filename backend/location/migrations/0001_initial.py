# Generated by Django 2.2.8 on 2020-03-23 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0015_auto_20200204_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('country', models.CharField(max_length=255, unique=True)),
                ('location', models.CharField(max_length=255, unique=True)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='profiles.Profile')),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
                'ordering': ['-id'],
            },
        ),
    ]
