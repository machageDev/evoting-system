# Generated by Django 5.1.6 on 2025-02-19 14:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("webapp", "0003_post_candidate_position_candidate_profile_picture_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="candidate",
            name="election",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="webapp.election",
            ),
        ),
    ]
