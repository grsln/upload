# Generated by Django 3.1 on 2020-08-07 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='cover',
            new_name='image',
        ),
    ]
