# Generated by Django 4.0.5 on 2022-10-20 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0011_alter_books_is_finished'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Books',
        ),
    ]