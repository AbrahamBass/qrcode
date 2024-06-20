import io
import pytest
from app.main import app
from PIL import Image   
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.mark.parametrize(
        "route, params, expected",
        [
            ("/link", {"website": "example.com"}, "image/png")
        ]
)
def test_qr_router(route, params, expected):
    response = client.get(route, params=params)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == expected
    image = Image.open(io.BytesIO(response.content))
    assert image.format.lower() == "png"

