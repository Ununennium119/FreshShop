# Generated by Django 4.1.2 on 2022-10-15 15:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0020_alter_productreview_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="productreview",
            options={"ordering": ["-create_time"]},
        ),
        migrations.RemoveField(
            model_name="productreview",
            name="create_date",
        ),
        migrations.AddField(
            model_name="productreview",
            name="create_time",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
