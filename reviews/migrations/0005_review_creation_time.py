# Generated by Django 4.2.5 on 2023-09-11 12:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_review_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='creation_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
