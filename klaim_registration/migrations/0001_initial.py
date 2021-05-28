# Generated by Django 3.2.2 on 2021-05-12 17:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Perusahaan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=200)),
                ('npp', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='DataKlaim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=200)),
                ('nik', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator('^\\d{6}([04][1-9]|[1256][0-9]|[37][01])(0[1-9]|1[0-2])\\d{2}\\d{4}$', 'Format NIK Tidak Sesuai')])),
                ('kpj', models.CharField(max_length=11)),
                ('tgl_lahir', models.DateField()),
                ('tempat_lahir', models.CharField(max_length=200)),
                ('alamat', models.CharField(max_length=250)),
                ('nama_ibu', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('1', 'BELUM MENIKAH'), ('2', 'MENIKAH')], default='1', max_length=1)),
                ('nama_pasangan', models.CharField(blank=True, max_length=100, null=True)),
                ('tgl_lahir_pasangan', models.DateField(blank=True, null=True)),
                ('nama_anak_s', models.CharField(blank=True, max_length=100, null=True)),
                ('tgl_lahir_s', models.DateField(blank=True, null=True)),
                ('nama_anak_d', models.CharField(blank=True, max_length=100, null=True)),
                ('tgl_lahir_d', models.DateField(blank=True, null=True)),
                ('no_hp', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^(08+[1-9])([0-9]{9})$', 'Format NO HP TIDAK SESUA!!!')])),
                ('nama_rekening', models.CharField(max_length=100)),
                ('no_rekening', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator('^\\d{6,}$', 'No Rekening Harus Berupa Angka')])),
                ('file_kk', models.FileField(upload_to='kk/', validators=[django.core.validators.RegexValidator('.*\\.(jpg|JPG|gif|GIF|doc|DOC|pdf|PDF)', 'Only Support PDF dan JPG')])),
                ('file_ktp', models.FileField(upload_to='ktp/', validators=[django.core.validators.RegexValidator('.*\\.(jpg|JPG|gif|GIF|doc|DOC|pdf|PDF)', 'Only Support PDF dan JPG')])),
                ('file_buku_nikah', models.FileField(upload_to='buku-nikah/', validators=[django.core.validators.RegexValidator('.*\\.(jpg|JPG|gif|GIF|doc|DOC|pdf|PDF)', 'Only Support PDF dan JPG')])),
                ('file_lain', models.FileField(blank=True, null=True, upload_to='lain/', validators=[django.core.validators.RegexValidator('.*\\.(jpg|JPG|gif|GIF|doc|DOC|pdf|PDF)', 'Only Support PDF dan JPG')])),
                ('created_on', models.DateField(auto_now_add=True)),
                ('npp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='klaim_registration.perusahaan')),
            ],
        ),
    ]