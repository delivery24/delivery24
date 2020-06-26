# Generated by Django 3.0.6 on 2020-06-25 22:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200621_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='verification_code',
            field=models.IntegerField(null=True, unique=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999)]),
        ),
    ]
