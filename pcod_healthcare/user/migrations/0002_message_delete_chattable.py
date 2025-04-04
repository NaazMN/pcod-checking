# Generated by Django 5.1.6 on 2025-03-18 14:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sender_id", models.IntegerField()),
                ("receiver_id", models.IntegerField()),
                ("content", models.TextField()),
                ("timestamp", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_read", models.BooleanField(default=False)),
            ],
            options={
                "ordering": ["timestamp"],
            },
        ),
        migrations.DeleteModel(
            name="Chattable",
        ),
    ]
