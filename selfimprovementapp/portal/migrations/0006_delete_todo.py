# Generated by Django 4.0.5 on 2022-10-16 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_todo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Todo',
        ),
    ]