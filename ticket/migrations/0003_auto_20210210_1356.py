# Generated by Django 3.1.5 on 2021-02-10 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20210209_1307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackimage',
            name='feedback',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedback_images', to='ticket.feedback'),
        ),
    ]
