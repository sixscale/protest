# Generated by Django 5.0.4 on 2024-06-07 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fulfilment', '0016_alter_fulfillmentfollowingstatuses_ff_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crmdealitem',
            old_name='item_price',
            new_name='price_in_euros',
        ),
        migrations.RemoveField(
            model_name='crmdealitem',
            name='total_price',
        ),
        migrations.AddField(
            model_name='crmdealinfo',
            name='cart_total_in_euros',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
