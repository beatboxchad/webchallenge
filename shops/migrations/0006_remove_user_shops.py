# Generated by Django 2.0.2 on 2018-03-08 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0005_auto_20180308_1752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='shops',
        ),
    ]
