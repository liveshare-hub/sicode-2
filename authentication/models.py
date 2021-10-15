# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as Img
from io import BytesIO
from django.db.models.signals import post_delete, post_save

    

from django.dispatch import receiver

from django.db import models
# import datetime


class Perusahaan(models.Model):
    nama = models.CharField(max_length=200)
    npp = models.CharField(max_length=8)

    class Meta:
        ordering = ['-npp']
        verbose_name = "NPP"
        verbose_name_plural = "LIST NPP"

    def __str__(self):
        return self.nama


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)
    propic = models.ImageField(
        upload_to='profile/hrd/', blank=True, null=True)
    npp = models.ForeignKey(Perusahaan, on_delete=models.CASCADE, blank=True, null=True)
    is_hrd = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        width = 70
        height = 70
        size = (width, height)
        isSame = False
        if self.propic:
            try:
                this = Profile.objects.get(id=self.id)
                if this.propic == self.propic:
                    isSame = True
            except:
                pass

            image = Img.open(
                BytesIO(self.propic.read()))
            (imw, imh) = image.size
            if (imw > width) or (imh > height):
                image.thumbnail(size, Img.ANTIALIAS)

            # If RGB, convert transparancy
            if image.mode == 'RGBA':
                image.load()
                background = Img.new("RGB", image.size, (255, 255, 255))
                # 3 is the alpha channel
                background.paste(image, mask=image.split()[3])
                image = background

            output = BytesIO()
            image.save(output, format='JPEG', quality=80)
            output.seek(0)
            self.propic = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.propic.name.split('.')[
                                               0], 'image/jpeg', output.getvalue, None)
        try:
            this = Profile.objects.get(id=self.id)
            if this.propic == self.propic or isSame:
                self.propic = this.propic
            else:
                this.propic.delete(save=False)
        except:
            pass

        super().save(*args, **kwargs)

@receiver(post_delete, sender=Profile)
def propic_post_delete_handler(sender, **kwargs):
    instance = kwargs['instance']
    storage, path = instance.propic.storage, instance.propic.path
    if (path != '.') and (path != '/') and (path != 'profile/') and (path != 'profile/.'):
        storage.delete(path)

@receiver(post_save, sender=User)
def testing_receiver(sender, instance, created, **kwargs):
    if created:
        print(instance)
        print(kwargs['signal'])
        print(sender)
        Profile.objects.create(user=instance)

