# Generated by Django 4.2.2 on 2024-02-25 11:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("swimming_app", "0024_subplan_validity_days_alter_assignsubscriber_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="subscription",
            name="reg_date",
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
