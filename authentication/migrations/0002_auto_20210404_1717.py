# Generated by Django 3.1.5 on 2021-04-04 14:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='about_me',
            field=models.TextField(max_length=1000, validators=[django.core.validators.MinLengthValidator(50, 'MinLengthValidator')]),
        ),
    ]