# Generated by Django 3.0.6 on 2020-06-17 21:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_email_confirmed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ik',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(30000000000), django.core.validators.MaxValueValidator(69999999999)], verbose_name='isikukood'),
        ),
    ]