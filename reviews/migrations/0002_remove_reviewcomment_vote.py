# Generated by Django 4.2.4 on 2023-09-07 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviewcomment',
            name='vote',
        ),
    ]
