# Generated by Django 2.0.2 on 2018-04-16 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0025_auto_20180416_0252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='balance',
        ),
    ]
