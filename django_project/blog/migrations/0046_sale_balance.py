# Generated by Django 2.0.2 on 2018-04-22 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0045_purchase_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='balance',
            field=models.CharField(default=0, max_length=200),
        ),
    ]
