# Generated by Django 2.0.2 on 2018-04-22 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0044_auto_20180421_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15, max_length=200),
        ),
    ]