# Generated by Django 4.0 on 2022-03-20 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.CharField(default='/local_store/\\profile_pics\\default.png', max_length=200),
        ),
    ]
