# Generated by Django 2.1.2 on 2019-02-10 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sport', '0008_auto_20190208_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resulttable',
            name='place',
            field=models.PositiveIntegerField(db_index=True, verbose_name='Место'),
        ),
    ]
