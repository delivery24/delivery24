# Generated by Django 3.0.6 on 2020-08-11 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20200811_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_start',
            field=models.DateTimeField(help_text='delivery start help text', verbose_name='delivery start'),
        ),
    ]