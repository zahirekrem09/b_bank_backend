# Generated by Django 3.1.5 on 2021-02-14 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0004_ticket_service_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'ordering': ('created_at',)},
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ('created_at',)},
        ),
    ]