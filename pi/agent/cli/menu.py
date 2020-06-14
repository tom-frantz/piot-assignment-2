"""
Console screen for AP menu.
"""
import sys
import agent.facial_recognition.recogniser as recogniser
from agent.qrcode_scanning.qrdecoder import QrDecoder
from agent.qrcode_scanning.img_retriever import Cv2Image
from agent.qrcode_scanning.img_retriever import FilePathException
from agent.qrcode_scanning.img_retriever import FileTypeException
import cv2
import traceback
from datetime import datetime


class Things:
    """
    Menu functions.
    """

    def login(self, send_queue, recv_queue):
        """
        Login for registered users.

        :param str username: required.
        :param str password: required.
        :param str car_number: required.
        """
        username = input("Please iuput your username:")
        print(username)
        password = input("Please input your password:")
        print(password)
        car_number = input("Please input your car number:")
        print(car_number)
        date = str(datetime.now())
        data = {
            "cmd": "login",
            "username": username,
            "password": password,
            "car_number": car_number,
            "time": date,
        }
        print(data)
        try:
            send_queue.put(data)
        except:
            traceback.print_exc()
        while 1:
            recv = recv_queue.get()
            if recv:
                break
        print("Login token generated:", recv)

    def qrcode_login(self, send_queue, recv_queue):
        """login with a qrcode
        
        Allows individuals to login using a supplied QRCode.

        :param str img_name: name of an image in images dir, required.
        :param str car_number: id of car, required.
        """
        car_number = input("Please input car number: ")

        # find qrcode and seperate data into username and password
        img_name = input("Please input QrCode image name (in form image.png): ")
        path = "agent/qrcode_scanning/images/"
        try:
            image = Cv2Image.read_image(path + img_name)
        except FilePathException as e:
            if e.code == 0:
                print(f"Fatal Error Occured:\n{e.msg}\n{e.code}")
            else:
                print("Filename Error")
            return
        except FileTypeException as e:
            print("Unsupported file type used")
            return
        
        #data should be in form of "username:password"
        decoder = QrDecoder()
        decoded = decoder.decode_img(image)
        qr_data_string = decoded.data.decode("utf-8")

        SEPERAND = ':'
        qr_data_list = qr_data_string.split(SEPERAND)
        if len(qr_data_list) != 2:
            # raise exception
            raise ValueError("Qr Code data is in illegal form")
        username = qr_data_list[0]
        password = qr_data_list[1]

        date = str(datetime.now())
        data = {
            "cmd": "login",
            "username": username,
            "password": password,
            "car_number": car_number,
            "time": date
        }
        # Send data
        try:
            send_queue.put(data)
        except:
            traceback.print_exc()
        while 1:
            recv = recv_queue.get()
            if recv:
                break
        print("Login token generated:", recv)

    def facial_recog_login(self, send_queue, recv_queue):
        recog = recogniser.Facialrecog()
        username = input("Enter username:")
        is_same_person = False
        cap = cv2.VideoCapture(0)
        if cap is None or not cap.isOpened():
            imgpath = input("Enter img name:")
            import_img_path = "pi/agent/facial_recognition/import/" + imgpath
            img = cv2.imread(import_img_path)
            is_same_person = recog.recog_image(username, img)
        else:
            is_same_person = recog.once_time_recog(username)

        if not is_same_person:
            print("Face not recognised")
            return
        # login to pi

    def unlock_car(self, send_queue, recv_queue):
        """
        Unlock car if booking is valid.

        :param int booking_number: required.
        :param str car_number: required.
        """
        booking_number = input("Please iuput your booking number:")
        car_number = input("Please iuput your car number:")
        data = {
            "cmd": "unlock_car",
            "booking_number": booking_number,
            "car_number": car_number,
        }
        try:
            send_queue.put(data)
        except:
            traceback.print_exc()
        while 1:
            recv = recv_queue.get()
            if recv:
                break
        print("Car {} unlocked successfully.".format(data['car_number']))

    def return_car(self, send_queue, recv_queue):
        """
        Return a car.

        :param int booking_number: required.
        :param str car_number: required.
        """
        booking_number = input("Please iuput your booking number:")
        print(booking_number)
        return_car_number = input("Please iuput your return car number:")
        print(return_car_number)
        data = {
            "cmd": "return_car",
            "booking_number": booking_number,
            "return_car_number": return_car_number,
        }
        try:
            send_queue.put(data)
        except:
            traceback.print_exc()
        while 1:
            recv = recv_queue.get()
            if recv:
                break


class Menu:
    """
    Menu display options.
    """

    def __init__(self):
        self.thing = Things()
        self.choices = {
            "1": self.thing.login,
            "2": self.thing.facial_recog_login,
            "3": self.thing.qrcode_login,
            "4": self.thing.unlock_car,
            "5": self.thing.return_car,
            "6": self.quit,
        }

    def display_menu(self):
        print(
            """
                 Operation Menu:
                 1. Login
                 2. Login with facial recognition
                 3. Login with QR Code
                 4. Unlock Car
                 5. Return Car
                 6. Quit"""
        )

    def run(self, send_queue, recv_queue):
        """
        Menu option input validation.
        """
        while True:
            self.display_menu()
            try:
                choice = input("Enter an option: ")
            except Exception:
                print("Please input a valid option!")
                continue

            choice = str(choice).strip()
            action = self.choices.get(choice)
            if action:
                action(send_queue, recv_queue)
            else:
                print("{0} is not a valid choice".format(choice))

    def quit(self):
        """
        Quit the menu.
        """
        print("\nThank you for using this script!\n")
        sys.exit(0)
