# Generated by Django 4.1.7 on 2023-04-02 19:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("engagement", "0003_userengagement_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userengagement",
            name="engagement_status",
            field=models.IntegerField(
                choices=[(3, "None"), (1, "Like"), (2, "Dislike")], default=3
            ),
        ),
    ]
