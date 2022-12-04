# Generated by Django 4.1.2 on 2022-10-07 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0010_alter_productcategory_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="discounted_price",
            field=models.DecimalField(
                decimal_places=2,
                default=models.DecimalField(decimal_places=2, max_digits=6),
                max_digits=6,
            ),
        ),
    ]