import unittest
import cv2
from img_retriever import Cv2Image
from img_retriever import FileTypeException
from img_retriever import FilePathException
from img_retriever import CameraNotAvailable


class Cv2ImageTest(unittest.TestCase):
    def setUp(self) -> None:
        pass

    @unittest.skip("No webcam present")
    def test_CaptureFromExistingWebcam_ImageReturned(self):
        Cv2Image.capture_image()

    def test_CaptureFromNonExistentWebcam_RaiseCameraNotAvailable(self):
        self.assertRaises(CameraNotAvailable, Cv2Image.capture_image, 8)

    def test_ReadExistingPNGOfDog_ReturnImageOfDog(self):
        path = "test_imgs/picture_of_dog__expected__raise_LessThanOneCode.jpg"
        img = cv2.imread(path)
        ret_img = Cv2Image.read_image(path)
        self.assertTrue((img == ret_img).all())

    def test_PathDoesNotExist_RaiseFilePathException(self):
        # path does not exist
        path = "test_imgs/cheese/file.png"
        self.assertRaises(FilePathException, Cv2Image.read_image, path)

    def test_FileDoesNotExist_RaiseFilePathException(self):
        path = "test_imgs/nonexistent.png"
        self.assertRaises(FilePathException, Cv2Image.read_image, path)

    def test_FileIsTXT_RaiseFileTypeException(self):
        path = "test_imgs/testfile.txt"
        self.assertRaises(FileTypeException, Cv2Image.read_image, path)

if __name__ == "__main__":
    unittest.main()
