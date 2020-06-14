import requests
import json
import sys, subprocess
import random

class Menu():

    def __init__(self):
        self.tokens = {}

    def login(self):
        """
        Login and check if the user is an authorised admin via RESTful API.
        ...
        :return: whether the user login is valid
        :rtype: bool
        """

        print("*************************")
        print("Admin Voice Search System")
        print("*************************")

        username = input("Please enter your username: ")
        password = input("Please enter your password: ")

        r = requests.post(
            'http://localhost:5000/auth/admin-check', 
            data = {'username':username, 'password': password})

        res = r.text

        try:
            self.tokens = json.loads(res)
            if self.tokens['role']== 'admin':
                print('\n')
                print("Now you can start your voice search.")
                print("Search with phrase: \"Car number [car_number]\".")
                return True
            else:
                print(
                    "Sorry your are not an authorised admin to use the system. \
                    Please login with a valid account.")
                return False
                
        except Exception as e:
            print('Error finding the user.')
            return False

    def search(self,car_number):
        """
        Search car in cloud database via RESTful AP
        """

        access_token = self.tokens['access_token']
        headers = {'Authorization': 'Bearer {}'.format(access_token)}
        url= 'http://localhost:5000/cars/detail/{}'.format(car_number)

        try:
            r = requests.get(url, headers=headers)
            res = r.text
            detail = json.loads(res)
            print(json.dumps(detail, indent=2))
        except Exception as e:
            print("Sorry, this car doesn't exist.")