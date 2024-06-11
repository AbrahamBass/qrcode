from io import BytesIO
from src.instances.qr_instance import Run
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from fastapi.responses import StreamingResponse


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
    async def Email():
        pass

