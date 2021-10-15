from django.contrib import admin

from .models import DataTK, ApprovalHRD, toQRCode

admin.site.register(DataTK)
# admin.site.register(Perusahaan)
# admin.site.register(DaftarHRD)
admin.site.register(ApprovalHRD)
admin.site.register(toQRCode)
