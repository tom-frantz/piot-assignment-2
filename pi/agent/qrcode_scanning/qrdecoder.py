from pyzbar.pyzbar import decode


class IncorrectCode(Exception):
    def __init__(self, msg, code=None):
        self.msg = msg
        if code:
            self.code = code


class LessThanOneCode(Exception):
    def __init__(self, msg, code=None):
        self.msg = msg
        if code:
            self.code = code


class MoreThanOneCode(Exception):
    def __init__(self, msg, code=None):
        self.msg = msg
        if code:
            self.code = code


class QrDecoder:
    def decode_img(self, img):
        """returns an image decoded into a qr codes data

        Takes an image parameter and decodes it, the result is then validated to ensure it contains only one qr code.

        :param img: a cv2 representation of an image, retrieved with cv2.imread(..)
        :return decoded: decoded image, i.e. the qr codes and it's data
        """
        decoded = decode(img)
        self._validate_decode(decoded)
        return decoded[0]

    def _validate_decode(self, decoded):
        """validates decoded data to be compliant with spec form

        Validates a decoded image to ensure it only contains one qr code, raises an error if not.

        :param decoded:
        :raises:
            ERR2: if decoded data does not contain a qr code
            ERR1: if decoded data contains more than one qr code
        """
        if not decoded:
            raise LessThanOneCode("No codes of any design were detected")
        if len(decoded) > 1:
            raise MoreThanOneCode("Too many codes exist in the image supplied")
        if decoded[0].type != "QRCODE":
            raise IncorrectCode("Code in image is not in qr code format, instead it is format " + decoded[0].type)

