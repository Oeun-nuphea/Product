# Generated by Django 5.1.7 on 2025-03-15 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_order_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='note',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
