"""
Console screen for AP menu.
"""
import sys
#import agent.facial_recognition.recogniser as recogniser
#import cv2
import time
import pexpect

Global_max_scan_time = 15


class Things:
    """
    Menu functions.
    """

    def login(self, send_queue, recv_queue):
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
            "time": date

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

    def facial_recog_login(self, send_queue, recv_queue):
        return True
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
            "car_number": car_number
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
            "return_car_number": return_car_number
        }
        try:
            send_queue.put(data)
        except:
            traceback.print_exc()
        while 1:
            recv = recv_queue.get()
            if recv:
                break

    def search_bluetooth(self, send_queue, recv_queue):
        child = pexpect.spawn("bluetoothctl")
        child.send("scan on\n")
        pre_input_mac = "F0:18:98:00:F5:79"
        start_time = time.time()
        try:
            while True:
                child.expect("Device (([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2}))")
                bdaddr = child.match.group(1)
                daddr_str = bytes.decode(bdaddr)
                if daddr_str == pre_input_mac:
                    child.send("scan off\n")
                    child.send("quit\n")
                    print('has found engineer devices, will process to login')
                    data = {
                        "engineer_mac": daddr_str
                    }
                    send_queue.put(data)
                    return True
                past_time = time.time()-start_time
                if past_time > Global_max_scan_time:
                    return False
                    # results.write(bdaddr+"\n")
        except KeyboardInterrupt:
            child.close()
            results.close()
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
            "3": self.thing.unlock_car,
            "4": self.thing.return_car,
            "5": self.thing.search_bluetooth,
            "6": self.quit,
        }

    def display_menu(self):
        print(
            """
                 Operation Menu:
                 1. Login
                 2. Login with facial recognition
                 3. Unlock Car
                 4. Return Car
                 5. Search Bluetooth
                 6. Quit
                 """
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
