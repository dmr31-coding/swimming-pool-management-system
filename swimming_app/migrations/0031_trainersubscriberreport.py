# Generated by Django 4.2.2 on 2024-02-28 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("swimming_app", "0030_trainermsg"),
    ]

    operations = [
        migrations.CreateModel(
            name="TrainerSubscriberReport",
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
                ("report_msg", models.TextField()),
                (
                    "report_for_trainer",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="report_for_trainer",
                        to="swimming_app.trainer",
                    ),
                ),
                (
                    "report_for_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="report_for_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "report_from_trainer",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="report_from_trainer",
                        to="swimming_app.trainer",
                    ),
                ),
                (
                    "report_from_user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="report_from_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
