# Generated by Django 2.2.8 on 2020-04-02 10:46

import certificates.models
from django.db import migrations, models
import main.management.validators.filevalidator


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0004_auto_20200402_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='document',
            field=models.FileField(blank=True, default='', upload_to=certificates.models.PathAndRename('images/2020/04/02'), validators=[main.management.validators.filevalidator.FileValidator(content_types=('image/jpeg', 'image/jpg'), max_size=2048000)]),
        ),
    ]
