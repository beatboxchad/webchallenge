# Generated by Django 2.0.2 on 2018-03-08 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0004_auto_20180307_2304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='shops',
        ),
        migrations.AddField(
            model_name='user',
            name='shops',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='shops.Shop'),
        ),
    ]
