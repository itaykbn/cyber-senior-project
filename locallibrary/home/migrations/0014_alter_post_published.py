# Generated by Django 4.0 on 2022-04-15 23:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_alter_categories_unique_together_alter_categories_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 16, 2, 5, 42, 24580)),
        ),
    ]
