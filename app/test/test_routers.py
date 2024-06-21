import io
import pytest
from app.main import app
from PIL import Image   
from fastapi.testclient import TestClient


client = TestClient(app)

@pytest.mark.parametrize(
        "route, params, expected",
        [
            ("/link", {"website": "example.com"}, "image/png"),
            ("/email", {"to": "abrixa12@gamil.com", "sub": "Comunicado", "body": "Mañana no hay clases"}, "image/png"),
            ("/text", {"message": "me gusta el chocolate"}, "image/png"),
            ("/whatsapp", {"phone": 3157761699, "message": "Hola, mas informacion"}, "image/png")
        ]
)
def test_qr_router_pass(route, params, expected):
    response = client.get(route, params=params)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == expected
    image = Image.open(io.BytesIO(response.content))
    assert image.format.lower() == "png"

