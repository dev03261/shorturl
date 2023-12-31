# Generated by Django 4.2.4 on 2023-09-11 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlshortener', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shortenedurl',
            name='original_url',
        ),
        migrations.AddField(
            model_name='shortenedurl',
            name='long_url',
            field=models.URLField(default='https://example.com'),
        ),
        migrations.AlterField(
            model_name='shortenedurl',
            name='short_url',
            field=models.CharField(max_length=20),
        ),
    ]
