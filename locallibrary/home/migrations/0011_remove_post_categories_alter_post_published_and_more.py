# Generated by Django 4.0 on 2022-04-15 13:44

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_post_categories_alter_post_published'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='categories',
        ),
        migrations.AlterField(
            model_name='post',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 15, 16, 43, 49, 555359)),
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('categorie', models.CharField(max_length=200, null=True)),
                ('id', models.CharField(default='<django.db.models.fields.related.ForeignKey>|<django.db.models.fields.CharField>', editable=False, max_length=100, primary_key=True, serialize=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.post')),
            ],
        ),
    ]