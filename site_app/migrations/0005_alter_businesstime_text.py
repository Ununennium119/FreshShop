# Generated by Django 4.1.2 on 2022-10-13 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("site_app", "0004_sitesetting_teammember_businesstime"),
    ]

    operations = [
        migrations.AlterField(
            model_name="businesstime",
            name="text",
            field=models.CharField(max_length=64),
        ),
    ]
