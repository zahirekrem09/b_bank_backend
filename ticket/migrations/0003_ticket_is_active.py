# Generated by Django 3.1.5 on 2021-04-14 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20210404_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
