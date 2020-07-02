# Generated by Django 3.0.6 on 2020-07-02 20:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200702_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='verification_code',
            field=models.CharField(max_length=4, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(4)]),
        ),
    ]
