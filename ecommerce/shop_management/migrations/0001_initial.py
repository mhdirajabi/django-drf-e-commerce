# Generated by Django 4.0 on 2021-12-28 22:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0009_alter_address_options_alter_profile_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'نوع فروشگاه',
                'verbose_name_plural': '\u200cانواع فروشگاه\u200cها',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='نام فروشگاه')),
                ('status', models.CharField(choices=[('confirmed', 'تأیید شده'), ('rejected', 'رد شده'), ('processing', 'در حال بررسی'), ('deleted', 'حذف شده')], default='processing', max_length=50, verbose_name='وضعیت')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop', to='accounts.customuser', verbose_name='صاحب فروشگاه')),
                ('type', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shop', to='shop_management.shoptype', verbose_name='نوع فروشگاه')),
            ],
            options={
                'verbose_name': 'فروشگاه',
                'verbose_name_plural': 'فروشگاه\u200cها',
            },
        ),
    ]
