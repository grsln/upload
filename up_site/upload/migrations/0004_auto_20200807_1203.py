# Generated by Django 3.1 on 2020-08-07 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0003_auto_20200807_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='filename',
            field=models.CharField(default='', max_length=100),
        ),
    ]