# Generated by Django 3.0.6 on 2020-06-17 22:36

import core.utils
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200617_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ik',
            field=models.BigIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(30000000000), django.core.validators.MaxValueValidator(69999999999), core.utils.ik_validator], verbose_name='isikukood'),
        ),
    ]