# Generated by Django 2.2.8 on 2020-04-01 19:32

import certificates.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='document',
            field=models.FileField(blank=True, default='', upload_to='', validators=[certificates.models.FileValidator(content_types=('image/jpeg', 'image/jpg'), max_size=2048000)]),
        ),
    ]
