# Generated by Django 5.0.4 on 2024-06-11 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fulfilment', '0019_remove_crmdealitem_item_id_remove_crmdealitem_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='fulfillmentfollowingstatuses',
            name='is_status_updated_in_crm',
            field=models.BooleanField(default=False),
        ),
    ]