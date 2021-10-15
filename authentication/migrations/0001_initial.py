# Generated by Django 3.2.8 on 2021-10-15 09:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perusahaan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=200)),
                ('npp', models.CharField(max_length=8)),
            ],
            options={
                'verbose_name': 'NPP',
                'verbose_name_plural': 'LIST NPP',
                'ordering': ['-npp'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propic', models.ImageField(blank=True, null=True, upload_to='profile/hrd/')),
                ('is_hrd', models.BooleanField(default=True)),
                ('npp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.perusahaan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]