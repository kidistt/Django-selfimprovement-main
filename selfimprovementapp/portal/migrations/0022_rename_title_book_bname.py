# Generated by Django 4.0.5 on 2022-12-08 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0021_book'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='title',
            new_name='bname',
        ),
    ]
