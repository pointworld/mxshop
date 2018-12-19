# Generated by Django 2.1.4 on 2018-12-19 19:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_nums', models.IntegerField(default=0, verbose_name='goods nums')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='add time')),
            ],
            options={
                'verbose_name': 'order goods',
                'verbose_name_plural': 'order goods',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_sn', models.CharField(blank=True, max_length=30, null=True, unique=True, verbose_name='order serial number')),
                ('trade_no', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='trade number')),
                ('pay_status', models.CharField(choices=[('success', 'trade success'), ('cancel', 'trade cancel'), ('paying', 'waiting for paying')], default='paying', max_length=20, verbose_name='pay status')),
                ('pay_type', models.CharField(choices=[('alipay', 'alipay'), ('wechat', 'wechat')], default='alipay', max_length=20, verbose_name='pay type')),
                ('order_additional_msg', models.CharField(max_length=200, verbose_name='message left by user')),
                ('order_amount', models.FloatField(default=0.0, verbose_name='order amount')),
                ('pay_time', models.DateTimeField(blank=True, null=True, verbose_name='pay time')),
                ('address', models.CharField(default='', max_length=100, verbose_name='to shipping address')),
                ('signer_name', models.CharField(default='', max_length=20, verbose_name='signer name')),
                ('signer_mobile', models.CharField(max_length=11, verbose_name='signer mobile')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='add time')),
            ],
            options={
                'verbose_name': 'order info',
                'verbose_name_plural': 'order info',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nums', models.IntegerField(default=0, verbose_name='bought nums')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='add time')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='goods')),
            ],
            options={
                'verbose_name': 'Cart',
            },
        ),
    ]
