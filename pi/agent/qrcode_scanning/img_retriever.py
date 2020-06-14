import cv2
import time
import os


class FileTypeException(Exception):
    def __init__(self, msg, code=None):
        self.msg = msg
        if code:
            self.code = code


class FilePathException(Exception):
    def __init__(self, msg, code=None):
        self.msg = msg
        if code:
            self.code = code


class CameraNotAvailable(Exception):
    def __init__(self, msg, code=None):
        self.msg = msg
        if code:
            self.code = code


class Cv2Image:
    """Class for retrieving images using opencv

    This class retrieves images using the opencv library from a location of the hard drive or via a webcam if one is
    available. Methods are static as they don't require any stored variable data

    """

    @staticmethod
    def capture_image(camera=0):
        """captures and returns an image from a webcam

        captures and returns an image from a webcam if one is available

        :param camera: dictates the camera to be used, defaultss to one
        :return image: the cv2 representation of an image
        """
        cam = cv2.VideoCapture(camera)
        if cam is None or not cam.isOpened():
            raise CameraNotAvailable(f"Camera {camera} is not available")
        # Warm up the camera, sleep for ten seconds and take 50 captures to clear buffer
        cam.read()
        for i in range(50):
            time.sleep(0.2)
            cam.read()
        image = cam.read()

        return image

    @staticmethod
    def read_image(path_to_img):
        """reads an image form local memory

        reads an image from local memory and returns it

        :param path_to_img: path to the image to be read, must include file extension
        :return image: the cv2 representation of an image
        """
        # check path does not exist
        path, file_name = os.path.split(path_to_img)
        if not path:
            raise FilePathException("Directory does not exist",0)
        # check file does not exist
        if not os.path.isfile(path_to_img):
            raise FilePathException("File does not exist",1)
        # check file type is usable
        allowed_file_types = ("PNG", "JPEG", "JPG")
        upper_path = path_to_img.upper()
        is_available = False
        for substring in allowed_file_types:
            if upper_path.find(substring) != -1:
                is_available = True

        if not is_available:
            raise FileTypeException("File type not in accepted format")
        image = cv2.imread(path_to_img)

        return image
