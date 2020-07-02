# Generated by Django 3.0.6 on 2020-07-02 20:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_date',
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_end',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='delivery end date-time'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_start',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='delivery start date-time'),
            preserve_default=False,
        ),
    ]