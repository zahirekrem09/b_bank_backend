# Generated by Django 3.1.5 on 2021-03-25 10:36

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=250, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('birth_date', models.DateTimeField(blank=True, null=True)),
                ('gender', models.IntegerField(choices=[(0, 'male'), (1, 'female'), (2, 'not specified')], default=2)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('zip_address', models.CharField(max_length=8)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('service_type', models.IntegerField(choices=[(0, 'kapper'), (1, 'schoonheidsspecialiste'), (2, 'pedicure'), (3, 'visagist'), (4, 'styliste'), (5, 'nagelstyliste'), (6, 'haarwerken'), (7, 'not specified')], default=7)),
                ('for_gender', models.IntegerField(choices=[(0, 'male'), (1, 'female'), (2, 'not specified')], default=2)),
                ('schedule_for_client', models.DateTimeField(auto_now=True)),
                ('schedule_for_connector', models.DateTimeField(auto_now=True)),
                ('reserved_capacity', models.IntegerField(default=0)),
                ('latitude', models.CharField(blank=True, max_length=200, null=True)),
                ('longitude', models.CharField(blank=True, max_length=200, null=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('phone_number2', models.CharField(blank=True, max_length=20, null=True)),
                ('twitter_account', models.URLField(blank=True, max_length=300, null=True)),
                ('instagram_account', models.URLField(blank=True, max_length=300, null=True)),
                ('facebook_account', models.URLField(blank=True, max_length=300, null=True)),
                ('youtube_account', models.URLField(blank=True, max_length=300, null=True)),
                ('about_me', models.TextField(max_length=1500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('transportation_type', models.IntegerField(choices=[(0, 'bus'), (1, 'metro'), (2, 'taxi'), (3, 'not specified')], default=3)),
                ('preferred_lang', models.IntegerField(choices=[(0, 'dutch'), (1, 'english'), (2, 'not specified')], default=2)),
                ('expectation', models.CharField(blank=True, max_length=200, null=True)),
                ('profile_image', models.ImageField(blank=True, default='default-avatar-icon.png', null=True, upload_to=authentication.models.user_directory_path)),
                ('is_active', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_gray', models.BooleanField(default=False)),
                ('is_client', models.BooleanField(default=False)),
                ('is_pro', models.BooleanField(default=False)),
                ('is_sponsor', models.BooleanField(default=False)),
                ('is_connector', models.BooleanField(default=False)),
                ('gdpr_consent', models.BooleanField(default=False)),
                ('min_incomer', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
    ]
