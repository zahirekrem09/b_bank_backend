# Generated by Django 3.1.5 on 2021-02-13 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_auto_20210210_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='service_type',
            field=models.IntegerField(choices=[(0, 'kapper'), (1, 'schoonheidsspecialiste'), (2, 'pedicure'), (3, 'visagist'), (4, 'styliste'), (5, 'nagelstyliste'), (6, 'haarwerken'), (7, 'not specified')], default=7),
        ),
    ]