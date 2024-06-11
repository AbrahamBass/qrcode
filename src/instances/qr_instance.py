from qrcode import main, constants


def Run():
    qr = main.QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    return qr
