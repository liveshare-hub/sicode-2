# Generated by Django 3.2.3 on 2021-06-09 15:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('klaim_registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='toqrcode',
            name='url_uuid',
            field=models.UUIDField(default=uuid.UUID('1914dd2a-4711-4b48-b0f0-dafaa7825afc'), editable=False),
        ),
    ]
