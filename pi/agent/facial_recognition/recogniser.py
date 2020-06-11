import os
import time
import cv2
import pickle
import face_recognition
import imutils
from imutils import paths
from datetime import datetime


class Facialrecog:
    def __init__(self):
        self.database = "./dataset/"

    def recog_image(self, user_id: str, img) -> bool:
        return self._recognise(user_id, img)

    def once_time_recog(self, user_id: str) -> bool:
        """
        Capture image for recognition.
        """
        # Capture image
        cam = cv2.VideoCapture(0)
        cam.set(3, 640)
        cam.set(4, 480)
        # allow time for camera sensor to work, discard wamupframes
        cam.read()
        time.sleep(2.0)
        for i in range(1, 50):
            cam.read()
        captured, cap = cam.read()
        if not captured:
            raise Exception("Camera not able to capture")
        return self._recognise(user_id, cap)

    def add_image(self, user_id: str, img):
        if not user_id:
            raise Exception("Invalid Argument, user_id not supplied")
        if not img.any():
            raise Exception("Invalid Argument, img not supplied")

        directory = self.database + user_id
        if not os.path.exists(directory):
            os.makedirs(directory)
        self._store_image(user_id, img)

    def _recognise(self, user_id: str, img) -> bool:
        data = pickle.loads(open('encodings.pickle', 'rb').read())

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = imutils.resize(img, width=500)

        # detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # rects = detector.detectMultiScale(gray, scaleFactor=1.1,
        # minNeighbors=5, minSize=(20, 20))

        # boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
        boxes = face_recognition.face_locations(img, model="hog")

        encodings = face_recognition.face_encodings(img, boxes)
        names = []
        for encoding in encodings:
            matches = face_recognition.compare_faces(
                known_face_encodings="encodings.pickle", face_encoding_to_check=encoding
            )
            name = ""
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
            names.append(name)
        # Validate to ensure:
        # only one name/person was recognised: raise exception
        # a person was recognised: return false
        if user_id in names:
            return True
        return False

    def _store_image(self, user_id: str, img):
        if not user_id:
            raise Exception("Invalid Argument, user_id not supplied")
        if not img.any():
            raise Exception("Invalid Argument, img not supplied")
        directory = self.database + user_id
        if not os.path.exists(directory):
            raise Exception("Path does not exist, use add_image() to create a path")
        # Add to dataset of images
        img_file = directory + "/" + datetime.now().strftime("%d%m%Y%H%M%S") + '.jpg'
        # resize image to preserve precious memory
        img = imutils.resize(img, width=500)
        cv2.imwrite(img_file, img)
        self._encode_database()

    def _encode_database(self):
        knownEncodings = []
        knownNames = []
        imagePaths = list(paths.list_images("dataset"))
        for (i, imagePath) in enumerate(imagePaths):
            # get name from path
            name = imagePath.split(os.path.sep)[-2]
            # load input image
            img = cv2.imread(imagePath)
            # convert image
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # grab each face in image and cast bounding boxes
            boxes = face_recognition.face_locations(rgb, model="hog")
            encodings = face_recognition.face_encodings(rgb, boxes)
            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(name)
        data = {'encodings': knownEncodings, 'names': knownNames}
        with open('encodings.pickle', 'wb') as f:
            f.write(pickle.dumps(data))
