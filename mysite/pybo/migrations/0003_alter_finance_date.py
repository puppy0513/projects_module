# Generated by Django 3.2.8 on 2021-10-07 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0002_finance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finance',
            name='Date',
            field=models.DateTimeField(),
        ),
    ]
