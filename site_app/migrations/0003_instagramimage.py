# Generated by Django 4.1.2 on 2022-10-12 19:39

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("site_app", "0002_alter_sliderimage_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="InstagramImage",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("image", models.ImageField(upload_to="instagram")),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
    ]