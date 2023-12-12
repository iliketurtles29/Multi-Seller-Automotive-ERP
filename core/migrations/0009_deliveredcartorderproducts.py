# Generated by Django 4.2.6 on 2023-12-08 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_product_digital'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveredCartOrderProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(max_length=200)),
                ('item', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=200)),
                ('qty', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default='4.99', max_digits=9999999999)),
                ('total', models.DecimalField(decimal_places=2, default='4.99', max_digits=9999999999)),
                ('paid_status', models.BooleanField(default=False)),
                ('order_date', models.DateField(auto_now_add=True)),
                ('product_status', models.CharField(choices=[('Processing', 'Order Placed'), ('Preparing', 'Preparing to Ship'), ('Shipped', 'In Transit'), ('Delivered', 'Delivered')], default='Processing', max_length=35)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.address')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cartorder')),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivered_order_products', to='core.vendor')),
            ],
        ),
    ]
