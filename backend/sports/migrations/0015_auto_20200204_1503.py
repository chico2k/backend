# Generated by Django 2.2.8 on 2020-02-04 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0014_auto_20200204_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sport',
            name='sporttype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sporttype', to='sports.Sporttype'),
        ),
    ]
