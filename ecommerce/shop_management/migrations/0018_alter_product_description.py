# Generated by Django 3.2.10 on 2022-01-08 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_management', '0017_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='توضیحات محصول'),
        ),
    ]
