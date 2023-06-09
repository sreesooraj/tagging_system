# Generated by Django 4.1.7 on 2023-04-02 18:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("engagement", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="user_engagement",
            field=models.ManyToManyField(
                related_name="user_engagement",
                through="engagement.UserEngagement",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
