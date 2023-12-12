# Generated by Django 4.2.6 on 2023-12-09 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_delete_deliveredcartorderproducts'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilteredCartOrderProducts',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('core.cartorderproducts',),
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='authentic_rating',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='chat_resp_time',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='days_return',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='shipping_on_time',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='warranty_period',
        ),
    ]
