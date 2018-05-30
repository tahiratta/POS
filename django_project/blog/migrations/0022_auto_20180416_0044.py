# Generated by Django 2.0.2 on 2018-04-16 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_remove_supplier_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='author',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='customer_ledger',
            name='author',
        ),
        migrations.RemoveField(
            model_name='customer_ledger',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='product',
            name='author',
        ),
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='author',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='author',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='supplier_ledger',
            name='author',
        ),
        migrations.RemoveField(
            model_name='supplier_ledger',
            name='slug',
        ),
    ]