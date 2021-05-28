import uuid
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


def autoGen(nama):
    qrcode_image = qrcode.make(nama)
    canvas = Image.new('RGB', (290, 290), 'white')
    draw = ImageDraw.Draw(canvas)
    canvas.paste(qrcode_image)
    uid = uuid.uuid4()
    fname = f'{uid}.PNG'
    buffer = BytesIO()
    canvas.save(buffer, 'PNG')
