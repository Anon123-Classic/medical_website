# Generated by Django 5.1.3 on 2024-11-14 08:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicall', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='department',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='phone',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('^\\d{10}$', 'Phone number must be 10 digits.')]),
        ),
    ]
