# Generated by Django 2.0.2 on 2018-04-11 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20180411_0508'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(help_text='Slug will be generated automatically from the title of the post', unique=True)),
                ('description', models.CharField(blank=True, max_length=5000)),
                ('barcode', models.CharField(max_length=200)),
                ('brand', models.CharField(max_length=200)),
                ('colour', models.CharField(blank=True, max_length=200)),
                ('cost', models.CharField(max_length=200)),
                ('salePrice', models.CharField(max_length=200)),
                ('quantity', models.CharField(max_length=200)),
                ('bill', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Author')),
            ],
        ),
    ]
