# Generated by Django 2.0.2 on 2018-04-27 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0062_remove_invoice_sale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='product',
        ),
    ]