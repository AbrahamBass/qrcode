from pyzbar.pyzbar import decode
import tempfile
from PIL import Image
from io import BytesIO
from qrcode.main import QRCode
from qrcode.image.base import BaseImage
from app.instances.qr_instance import Run
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from fastapi.responses import StreamingResponse, PlainTextResponse
from fastapi import UploadFile, HTTPException


def QrResponse(qr: QRCode[BaseImage]):
    try:
        img = qr.make_image(
            image_factory=StyledPilImage,
            color_mask=RadialGradiantColorMask()
        )

        img_bytes_io = BytesIO()
        img.save(img_bytes_io, format='PNG')
        img_bytes_io.seek(0)

        return StreamingResponse(img_bytes_io, media_type="image/png")
    except:
        raise Exception('Error creating the QR image')


class QrController:

    @staticmethod
    async def Link(website: str):
        try:
            qr = Run()
            qr.add_data(website)

            return QrResponse(qr)
        except Exception as e:
            raise HTTPException(status_code=422, detail=e.args)

    @staticmethod
    async def Email(to: str, sub: str, body: str):
        try:
            qr = Run()
            qr.add_data(f"MATMSG:TO:{to};SUB:{sub};BODY:{body};;")

            return QrResponse(qr)
        except Exception as e:
            raise HTTPException(status_code=422, detail=e.args)

    @staticmethod
    async def Text(message: str):
        try:
            qr = Run()
            qr.add_data(message)

            return QrResponse(qr)
        except Exception as e:
            raise HTTPException(status_code=422, detail=e.args)

    @staticmethod
    async def Whatsapp(phone: int, message: str):
        try:
            qr = Run()
            qr.add_data(f"https://wa.me/{phone}/?text={message}")

            return QrResponse(qr)
        except Exception as e:
            raise HTTPException(status_code=422, detail=e.args)

    @staticmethod
    async def Read(file: UploadFile):

        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            temp_file_path = tmp.name
            content = await file.read()
            tmp.write(content)

        image = Image.open(temp_file_path)

        decoded_objects = decode(image)

        if decoded_objects:
            data = decoded_objects[0].data.decode('utf-8')
            return data

        raise HTTPException(status_code=422, detail="QR code not found")
