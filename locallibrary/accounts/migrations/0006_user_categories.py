# Generated by Django 4.0 on 2022-04-15 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='categories',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
