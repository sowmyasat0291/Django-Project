# Generated by Django 5.1.1 on 2024-09-24 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0002_alter_cartitem_cart_alter_cartitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
