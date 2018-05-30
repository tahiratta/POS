# Generated by Django 2.0.2 on 2018-04-16 08:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0023_auto_20180416_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=700),
        ),
        migrations.AlterField(
            model_name='customer',
            name='contact',
            field=models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='address',
            field=models.CharField(max_length=700),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='brandName',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='contact',
            field=models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
