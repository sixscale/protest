# Generated by Django 5.0.4 on 2024-05-22 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fulfilment', '0008_alter_fulfillmentcrmconnections_crm_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fulfillmentcrmconnections',
            name='ff_product_code',
            field=models.CharField(max_length=255),
        ),
    ]