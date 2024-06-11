import base64
from io import BytesIO
from src.instances.qr_instance import Run
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from fastapi.responses import StreamingResponse
from fastapi import UploadFile


def ResponseQr():
    pass


class QrController:

    @staticmethod
    async def Link(website: str):
        qr = Run()
        qr.add_data(website)

        img = qr.make_image(
            image_factory=StyledPilImage,
            color_mask=RadialGradiantColorMask()
        )

        img_bytes_io = BytesIO()
        img.save(img_bytes_io, format='PNG')
        img_bytes_io.seek(0)

        return StreamingResponse(img_bytes_io, media_type="image/png")

    @staticmethod
    async def Email(to: str, sub: str, body: str):
        qr = Run()
        qr.add_data(f"MATMSG:TO:{to};SUB:{sub};BODY:{body};;")

        img = qr.make_image(
            image_factory=StyledPilImage,
            color_mask=RadialGradiantColorMask()
        )

        img_bytes_io = BytesIO()
        img.save(img_bytes_io, format='PNG')
        img_bytes_io.seek(0)

        return StreamingResponse(img_bytes_io, media_type="image/png")

    @staticmethod
    async def Text(message: str):
        qr = Run()
        qr.add_data(message)

        img = qr.make_image(
            image_factory=StyledPilImage,
            color_mask=RadialGradiantColorMask()
        )

        img_bytes_io = BytesIO()
        img.save(img_bytes_io, format='PNG')
        img_bytes_io.seek(0)

        return StreamingResponse(img_bytes_io, media_type="image/png")

    @staticmethod
    async def Whatsapp(phone: int, message: str):
        qr = Run()
        qr.add_data(f"https://wa.me/{phone}/?text={message}")

        img = qr.make_image(
            image_factory=StyledPilImage,
            color_mask=RadialGradiantColorMask()
        )

        img_bytes_io = BytesIO()
        img.save(img_bytes_io, format='PNG')
        img_bytes_io.seek(0)

        return StreamingResponse(img_bytes_io, media_type="image/png")

    @staticmethod
    async def Image(file: UploadFile):
        image_bytes = await file.read()

        image_base64 = base64.b64encode(image_bytes).decode()

        qr_content = f"data:image/jpeg;base64,{image_base64}"

        qr = Run()
        qr.add_data(qr_content)
        qr.make(fit=True)

        img = qr.make_image(
            image_factory=StyledPilImage,
            color_mask=RadialGradiantColorMask()
        )

        img_bytes_io = BytesIO()
        img.save(img_bytes_io, format='PNG')
        img_bytes_io.seek(0)

        return StreamingResponse(img_bytes_io, media_type="image/png")
