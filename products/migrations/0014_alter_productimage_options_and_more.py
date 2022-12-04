# Generated by Django 4.1.2 on 2022-10-08 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0013_alter_productimage_id_productvisit"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="productimage",
            options={},
        ),
        migrations.RemoveField(
            model_name="productimage",
            name="is_main",
        ),
        migrations.AddField(
            model_name="product",
            name="main_image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
