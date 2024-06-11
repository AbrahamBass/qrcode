from qrcode import main, constants


def Run():
    try:
        qr = main.QRCode(
            version=None,
            error_correction=constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        return qr
    except Exception as e:
        print(e)
