import cv2
import tempfile
from pyzbar.pyzbar import decode
from io import BytesIO
from qrcode.main import QRCode
from qrcode.image.base import BaseImage
from src.instances.qr_instance import Run
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

        image = cv2.imread(temp_file_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        decode_objects = decode(gray_image)

        if decode_objects:
            for obj in decode_objects:
                data = obj.data.decode('utf-8')
                return PlainTextResponse(content=data)
        else:
            raise HTTPException(status_code=404, detail="Item not found")
