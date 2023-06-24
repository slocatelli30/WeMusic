# Generated by Django 4.1.4 on 2023-06-24 20:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wmapp', '0009_account_birth_date_alter_album_pub_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='sex',
            field=models.CharField(choices=[(0, 'Femmina'), (1, 'Maschio')], max_length=7, null=True),
        ),
        migrations.AlterField(
            model_name='album',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 24, 22, 25, 26, 270560), verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 24, 22, 25, 26, 270560), verbose_name='creation date'),
        ),
    ]
