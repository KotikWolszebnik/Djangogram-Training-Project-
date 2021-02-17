# Generated by Django 3.1.5 on 2021-02-17 18:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangogramm', '0014_auto_20210217_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='uploader',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_pictures', to=settings.AUTH_USER_MODEL),
        ),
    ]
