# Generated by Django 2.1.2 on 2019-02-08 02:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0003_place_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='name',
        ),
    ]