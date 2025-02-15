# Generated by Django 5.1.6 on 2025-02-11 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='election',
            name='active',
        ),
        migrations.AlterField(
            model_name='election',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='election',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('active', 'Active')], default='pending', max_length=10),
        ),
    ]
