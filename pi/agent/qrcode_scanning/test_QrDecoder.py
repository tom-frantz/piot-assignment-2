import unittest
import cv2
from qrdecoder import QrDecoder
from qrdecoder import IncorrectCode
from qrdecoder import LessThanOneCode
from qrdecoder import MoreThanOneCode


class QrDecoderTest(unittest.TestCase):
    """class for unit testing of QrDecoder

    Class for unit testing the QrDecoder class, this takes images and validates them after decoding the image into
    data from barcodes like QRCodes and code128's.

    """
    def setUp(self):
        self.decoder = QrDecoder()

    def test_OneQrCode_returnDecodedData(self):
        image = cv2.imread("test_imgs/single_qrcode__expected__engineer_name.png")
        decoded = self.decoder.decode_img(image)
        self.assertEqual("engineer_name", decoded.data.decode("utf-8"))

    def test_OneRotatedQrCode_returnDecodedData(self):
        image = cv2.imread("test_imgs/single_rotated_qrcode__expected__engineer_name.png")
        decoded = self.decoder.decode_img(image)
        self.assertEqual("engineer_name", decoded.data.decode("utf-8"))

    def test_OneCode128_raiseIncorrectCode(self):
        image = cv2.imread("test_imgs/code128_barcode__expected__raise_IncorrectCode.png")
        self.assertRaises(IncorrectCode, self.decoder.decode_img, image)

    def test_TwoQrCodes_RaiseMoreThanOneCode(self):
        image = cv2.imread("test_imgs/twoQrCodes__expected__MoreThanOneCode.png")
        self.assertRaises(MoreThanOneCode, self.decoder.decode_img, image)

    def test_PictureOfDog_RaiseLessThanOneCode(self):
        image = cv2.imread("test_imgs/picture_of_dog__expected__raise_LessThanOneCode.jpg")
        self.assertRaises(LessThanOneCode, self.decoder.decode_img, image)

if __name__ == "__main__":
    unittest.main()
