# Generated by Django 3.0.6 on 2020-10-22 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20201021_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='car_type',
            field=models.IntegerField(choices=[(1, 'S'), (2, 'M'), (3, 'L')], default=3, verbose_name='car type'),
        ),
    ]