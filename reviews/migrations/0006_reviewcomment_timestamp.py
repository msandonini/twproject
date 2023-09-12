# Generated by Django 4.2.5 on 2023-09-11 19:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_review_creation_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewcomment',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]