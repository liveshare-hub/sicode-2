from django.core.mail import EmailMultiAlternatives
from klaim_registration.models import toQRCode
# from core.settings import EMAIL_HOST_USER
from django.conf import settings
# from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags


def kirimEmail(id):
    # variables = {}
    data = toQRCode.objects.select_related('tk_klaim').get(tk_klaim__klaim__user__id=id)
    mail_title = u"AKUN ANDA TELAH BERHASIL DIBUAT"
    host = settings.EMAIL_HOST_USER
    to_mail = data.tk_klaim.klaim.email
    user = data.tk_klaim.klaim.user.username
    nama = data.tk_klaim.klaim.nama
    qrcode = data.img_svg
    # print(EMAIL_HOST_USER)
    # print(user)
    # print(qrcode)
    context = {
	'nama':nama,
	'username':user,
	'qrcode':qrcode
	}

    html = render_to_string('accounts/email.html', context)
    text = strip_tags(html)

    msg = EmailMultiAlternatives(
        mail_title,
        text,
        host,
        [to_mail],
    )
    # print(msg)
    msg.attach_alternative(html, "text/html")
    msg.attach_file(qrcode)
    msg.send()
