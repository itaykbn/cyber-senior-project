# Generated by Django 4.0 on 2022-03-20 01:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_post_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 20, 3, 36, 54, 301241)),
        ),
    ]