# Generated by Django 4.0.5 on 2022-10-20 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0013_books'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='status',
        ),
        migrations.AddField(
            model_name='books',
            name='is_finished',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='books',
            name='notes',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='books',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
