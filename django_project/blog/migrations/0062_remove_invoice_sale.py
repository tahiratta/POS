# Generated by Django 2.0.2 on 2018-04-26 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0061_invoice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='sale',
        ),
    ]
