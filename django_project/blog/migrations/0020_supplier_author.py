# Generated by Django 2.0.2 on 2018-04-16 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_remove_supplier_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Author'),
        ),
    ]