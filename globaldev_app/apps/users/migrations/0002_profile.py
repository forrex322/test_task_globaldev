# Generated by Django 3.2.13 on 2023-10-19 15:01

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('description', models.TextField(blank=True, default='', verbose_name="description of user's profile")),
                ('birth_date', models.DateField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(datetime.date(1910, 1, 1)), django.core.validators.MaxValueValidator(datetime.date.today)], verbose_name='Date of birth')),
                ('last_7_days_statistic', models.DurationField(blank=True, null=True)),
                ('last_30_days_statistic', models.DurationField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', related_query_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='related user')),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
            },
        ),
    ]
