# Generated by Django 3.1.5 on 2021-02-17 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangogramm', '0013_auto_20210217_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
