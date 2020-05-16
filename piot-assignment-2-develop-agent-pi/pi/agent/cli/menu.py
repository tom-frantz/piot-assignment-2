import sys
# from agent.sockets.send_master import *
import traceback
# import logging
# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
<<<<<<< HEAD
# logging.info
# DEBUG INFO WARNING ERROR CRITICAL


class Things:
    def login(self, send_queue, recv_queue):
=======
#logging.info
#DEBUG INFO WARNING ERROR CRITICAL

class Things:
    def login(self,send_queue,recv_queue):
>>>>>>> 323dc3290a55f16052f8fc4b7dc3229904098283
        username = input("Please iuput your username:")
        print(username)
        password = input("Please input your password:")
        print(password)
        data = {
<<<<<<< HEAD
            "cmd": "login",
            "username": username,
            "password": password,
        }
=======
            "cmd":"login",
            "username":username,
            "password":password,
        }
        print("will call the login method")
>>>>>>> 323dc3290a55f16052f8fc4b7dc3229904098283
        try:
            send_queue.put(data)
        except:
            traceback.print_exc()
        while 1:
            recv = recv_queue.get()
            if recv:
                break
<<<<<<< HEAD
        print("the login result is:", recv)

    def unlock_car(self, send_queue, recv_queue):
=======
        print("the login result is:",recv)

    def unlock_car(self,send_queue,recv_queue):
>>>>>>> 323dc3290a55f16052f8fc4b7dc3229904098283
        booking_number = input("Please iuput your booking number:")
        # logging.info(booking_number)
        car_number = input("Please iuput your car number:")
        data = {
<<<<<<< HEAD
            "cmd": "unlock_car",
            "booking_number": booking_number,
            "car_number": car_number,
=======
            "cmd":"unlock_car",
            "booking_number":booking_number,
            "car_number":car_number,
>>>>>>> 323dc3290a55f16052f8fc4b7dc3229904098283
        }
        try:
            send_queue.put(data)
        except:
            traceback.print_exc()
        while 1:
            recv = recv_queue.get()
            if recv:
                break

<<<<<<< HEAD
    def return_car(self, send_queue, recv_queue):
=======
    def return_car(self,send_queue,recv_queue):
>>>>>>> 323dc3290a55f16052f8fc4b7dc3229904098283
        booking_number = input("Please iuput your booking number:")
        print(booking_number)
        return_car_number = input("Please iuput your return car number:")
        print(return_car_number)


class Menu:
    def __init__(self):
        self.thing = Things()
        self.choices = {

            "1": self.thing.login,
            "2": self.thing.unlock_car,
            "3": self.thing.return_car,
            "4": self.quit,
        }

<<<<<<< HEAD
=======

>>>>>>> 323dc3290a55f16052f8fc4b7dc3229904098283
    def display_menu(self):
        print(
            """
                 Operation Menu:
                 1. Login
                 2. Unlock Car
                 3. Return Car
                 4. Quit"""
        )

<<<<<<< HEAD
    def run(self, send_queue, recv_queue):
=======
    def run(self,send_queue,recv_queue):
>>>>>>> 323dc3290a55f16052f8fc4b7dc3229904098283

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
<<<<<<< HEAD
                action(send_queue, recv_queue)
=======
                action(send_queue,recv_queue)
>>>>>>> 323dc3290a55f16052f8fc4b7dc3229904098283
            else:
                print("{0} is not a valid choice".format(choice))

    def quit(self):
        print("\nThank you for using this script!\n")
        sys.exit(0)
