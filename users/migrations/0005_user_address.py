# Generated by Django 4.1.2 on 2022-10-19 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_wishlistitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="address",
            field=models.TextField(blank=True, null=True),
        ),
    ]