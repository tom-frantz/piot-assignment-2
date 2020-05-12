import sys


class Things:
    def login(self):
        username = input("Please iuput your username:")
        print(username)
        password = input("Please input your password:")
        print(password)
        print("will call the login method")

    def unlock_car(self):
        booking_number = input("Please iuput your booking number:")
        print(booking_number)
        car_number = input("Please iuput your car number:")
        print(car_number)
        print("will call the unlock car method")

    def return_car(self):
        booking_number = input("Please iuput your booking number:")
        print(booking_number)
        return_car_number = input("Please iuput your return car number:")
        print(return_car_number)
        print("will call the return car method")


class Menu:
    def __init__(self):
        self.thing = Things()
        self.choices = {
            "1": self.thing.login,
            "2": self.thing.unlock_car,
            "3": self.thing.return_car,
            "4": self.quit,
        }

    def display_menu(self):
        print(
            """
                 Operation Menu:
                 1. Login
                 2. Unlock Car
                 3. Return Car
                 4. Quit"""
        )

    def run(self):
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
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def quit(self):
        print("\nThank you for using this script!\n")
        sys.exit(0)
