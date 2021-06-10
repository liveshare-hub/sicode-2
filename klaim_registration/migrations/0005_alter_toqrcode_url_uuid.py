# Generated by Django 3.2.3 on 2021-06-10 04:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('klaim_registration', '0004_alter_toqrcode_url_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toqrcode',
            name='url_uuid',
            field=models.UUIDField(default=uuid.UUID('22e8f548-9af1-4651-9462-e26f61115a01'), editable=False),
        ),
    ]