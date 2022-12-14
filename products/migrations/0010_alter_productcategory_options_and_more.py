# Generated by Django 4.1.2 on 2022-10-07 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0009_alter_productcategory_parent"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="productcategory",
            options={"ordering": ["name"], "verbose_name_plural": "product categories"},
        ),
        migrations.AlterModelOptions(
            name="productimage",
            options={"ordering": ["-is_main"]},
        ),
        migrations.AddField(
            model_name="product",
            name="discounted_price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
