# Generated by Django 4.1.2 on 2022-10-12 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0014_alter_productimage_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="main_image",
            field=models.ImageField(blank=True, null=True, upload_to="product-images"),
        ),
        migrations.AlterField(
            model_name="productimage",
            name="image",
            field=models.ImageField(upload_to="product-images"),
        ),
    ]
