# Generated by Django 2.0.2 on 2018-03-06 20:20

from django.db import migrations, models
import shops.models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0002_auto_20180305_2342'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', shops.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='shops',
            field=models.ManyToManyField(blank=True, to='shops.Shop'),
        ),
    ]
