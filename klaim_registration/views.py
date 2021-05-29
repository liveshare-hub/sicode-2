from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Subquery, OuterRef, IntegerField
from django.http import JsonResponse
# from dal import autocomplete
import random
import string

from django.core import serializers

from .form import DataKlaimForm
from .models import DataKlaim, Perusahaan, ApprovalHRD, DaftarHRD, toQRCode
from .decorators import admin_only


@login_required(login_url='/accounts/login/')
def index(request):
    user = request.user

    is_admin = User.objects.filter(username=user, is_superuser=True)

    is_hrd = DaftarHRD.objects.select_related(
        'user').filter(user__username=user)
    if is_admin:
        datas = DataKlaim.objects.all()
        size = datas.count()
    elif is_hrd:
        # return redirect('hrd-klaim')
        return redirect('get-detail')
    else:
        datas = DataKlaim.objects.filter(user=user).annotate(status_approve=Subquery(
            ApprovalHRD.objects.filter(klaim_id=OuterRef('pk')).values('status')[:1]))
        size = datas.count()
    context = {
        'datas': datas,
        'size': size,
    }

    return render(request, 'klaim_registration/index.html', context)


@login_required(login_url='/accounts/login/')
@admin_only
def tambahKlaim(request):
    # user = request.user
    # cekKlaim = ApprovalHRD.objects.select_related('klaim__user').filter(
    #     klaim__user__username=user, status='DISETUJUI')
    # if cekKlaim.exists():
    #     messages.warning(request, "Akun anda sudah pernah mengajukan KLAIM")
    #     return redirect(reverse('home-klaim'))
    # print(user.is_authenticated)
    if request.method == 'POST':
        forms = DataKlaimForm(request.POST, request.FILES)
        if forms.is_valid():
            post = forms.save(commit=False)
            # post.user = user
            post.user = user

            # post.npp = request.POST['npp']
            post.save()
            # hrd = DaftarHRD.objects.get(npp_id=post.npp_id)
            ApprovalHRD.objects.create(klaim_id=post.id, hrd_id=post.npp_id)
            toQRCode.objects.create(tk_klaim_id=post.id)

            return redirect('home-klaim')

    else:
        forms = DataKlaimForm()
    return render(request, 'klaim_registration/daftar.html', {'forms': forms})


@login_required(login_url='/accounts/login/')
@admin_only
def tambahKlaim1(request):
    if request.method == 'POST':
        forms = DataKlaimForm(request.POST, request.FILES)
        if forms.is_valid():
            post = forms.save(commit=False)
            random_str = string.ascii_letters+string.digits
            username = 'user_'+(''.join(random.choice(random_str)
                                        for i in range(4)))
            password = make_password('WELCOME1', salt=[username])
            cekUser = User.objects.all().filter(username=username)
            if cekUser.exists():
                messages.WARNING(request, "USER SUDAH DIPAKAI")
            else:
                post.user = User.objects.create(
                    username=username, password=password)
                post.save()
                ApprovalHRD.objects.create(
                    klaim_id=post.id, hrd_id=post.npp_id)
                toQRCode.objects.create(tk_klaim_id=post.id)
            return redirect('home-klaim')
    else:
        forms = DataKlaimForm()
    return render(request, 'klaim_registration/daftar.html', {'forms': forms})


@login_required(login_url='/accounts/login/')
def daftarKlaimHRD(request):
    # print(request.user)
    datas = ApprovalHRD.objects.select_related('hrd').filter(
        hrd__user__username=request.user, status='DALAM PEMERIKSAAN')
    if not datas.exists():
        datas = ApprovalHRD.objects.select_related(
            'hrd__user').filter(hrd__user__username=request.user)
        # detail = datas.select_related('klaim')
        # print(detail)
    if request.is_ajax:
        # print(request.POST.get('status'))
        ApprovalHRD.objects.filter(id=request.POST.get('id')).update(
            status=request.POST.get('status'), keterangan=request.POST.get('keterangan'))
        # return JsonResponse({'data': 'sucess'})
    context = {
        'datas': datas,
        # 'detail':detail,
    }

    return render(request, 'klaim_registration/hrd.html', context)


@ login_required(login_url='/accounts/login/')
def daftarKlaimHRD1(request):
    # print(request.user)
    datas = ApprovalHRD.objects.all().filter(
        hrd__user__username=request.user, status='DALAM PEMERIKSAAN')
    if not datas.exists():
        datas = ApprovalHRD.objects.all().filter(hrd__user__username=request.user)
        detail = datas.select_related('klaim')
        # print(detail)
    if request.is_ajax:
        # print(request.POST.get('status'))
        ApprovalHRD.objects.filter(id=request.POST.get('id')).update(
            status=request.POST.get('status'), keterangan=request.POST.get('keterangan'))
        # return JsonResponse({'data': 'sucess'})
    context = {
        'datas': datas,
        'detail': detail,
    }

    return render(request, 'klaim_registration/hrd1.html', context)


# @ login_required(login_url='/accounts/login/')
# def get_detail_tk(request, id=None):
#     instance = get_object_or_404(DataKlaim, id=id)
#     context = {
#         'instance': instance
#     }
#     return render(request, 'klaim_registration/modal.html', context)

@ login_required(login_url='/accounts/login/')
@admin_only
def get_klaimhrd_json(request, klaim_id):
    hrd_qs = list(toQRCode.objects.select_related('tk_klaim').filter(tk_klaim__hrd__user__username=request.user, tk_klaim__klaim_id=klaim_id).values(
        'tk_klaim_id', 'tk_klaim__klaim__nama', 'tk_klaim__klaim__nik', 'tk_klaim__klaim__kpj', 'tk_klaim__klaim__npp', 'tk_klaim__klaim__tempat_lahir', 'tk_klaim__klaim__tgl_lahir',
        'tk_klaim__klaim__nama_ibu', 'tk_klaim__klaim__status', 'tk_klaim__klaim__nama_rekening', 'tk_klaim__klaim__no_rekening', 'tk_klaim__klaim__no_hp'
    ))

    return JsonResponse({'data': hrd_qs})


def get_detail_tk(request):
    datas = toQRCode.objects.select_related('tk_klaim').filter(
        tk_klaim__hrd__user__username=request.user, tk_klaim__status='DALAM PEMERIKSAAN')
    if not datas.exists():
        datas = toQRCode.objects.select_related('tk_klaim').filter(
            tk_klaim__hrd__user__username=request.user)

    if request.is_ajax:

        ApprovalHRD.objects.filter(id=request.POST.get('id')).update(
            status=request.POST.get('status'), keterangan=request.POST.get('keterangan'))

    context = {
        'datas': datas
    }
    return render(request, 'klaim_registration/hrd.html', context)


@ login_required(login_url='/accounts/login/')
def daftarSeluruhKlaim(request):
    is_hrd = ApprovalHRD.objects.all().filter(
        hrd__user__username=request.user)[0]
    # print(is_hrd)
    if is_hrd:
        datas = is_hrd.all()
        return render(request, 'klaim_registration/hrd.html', {'datas': datas})
    else:
        return redirect('home-klaim')


def qrcode_display(request, id):

    qr_qs = list(toQRCode.objects.select_related('tk_klaim__klaim').filter(
        tk_klaim__hrd__user__username=request.user, id=id).values('tk_klaim_id', 'tk_klaim', 'url_uuid', 'img_svg'))

    return JsonResponse({'data': qr_qs})


def detail_tk(request, uid):
    datas = toQRCode.objects.select_related('tk_klaim').filter(
        url_uuid=uid)

    context = {
        'datas': datas
    }
    return render(request, 'klaim_registration/detail_tk.html', context)
