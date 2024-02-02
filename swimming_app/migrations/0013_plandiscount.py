# Generated by Django 5.0.1 on 2024-01-30 11:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("swimming_app", "0012_subplan_max_member"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlanDiscount",
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
                ("total_months", models.IntegerField()),
                ("total_discount", models.IntegerField()),
                (
                    "subplan",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="swimming_app.subplan",
                    ),
                ),
            ],
        ),
    ]
