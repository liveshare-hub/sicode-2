from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from django.contrib import messages


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'TK':
            messages.warning(
                request, "ANDA TIDAK MEMILIKI IZIN MENGAKSES MENU TERSEBUT!")
            return redirect(reverse('home-klaim'))

        if group == 'HRD':
            return view_func(request, *args, **kwargs)
    return wrapper_func
