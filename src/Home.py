import re
from src.Login import *
from Utilities.csv_connection import *
import getpass

class Home:
    lst_custdetails = []
    def __init__(self, login_obj,csv_con_obj ):
        self.login_obj = login_obj
        self.csv_con_obj = csv_con_obj

    def select_options(self):
        print('''Please Enter
                1 to Login
                2 to Register New Account
                3 to Exit''')
        try:
            options = int(input("Enter:"))
        except:
            print("Please select the correct option.")
            self.select_options()
        if(options ==1):
            self.login_obj.validate_login()
        elif(options ==2):
            print("\n****Create new Account*****")
            self.set_custname(input("Name: "))
            customerEmail = self.validate_email()
            customerPhone =  input("Phone: ")
            customerAge = input("Age:")
            customerPassword = input("Password:")
            Home.lst_custdetails.extend((self.get_custname(), customerEmail, customerPhone, customerAge, customerPassword))
            csv_connection.register_custdata_into_csv(Home.lst_custdetails)
            print("\nAccount registered successfully!!!\n")
            self.select_options()
        elif(options ==3):
            print("You are logged out")
            exit()
        else:
            print("Please select the correct option.")
            self.select_options()

    def validate_email(self):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        no_Of_Attempts, count = 3, 0
        for i in range(no_Of_Attempts):
            email = input("Email: ")
            if (re.fullmatch(regex, email)):
                return email
            else:
                count += 1
                if (count == no_Of_Attempts):
                    print("Failed to register, Program has exit!!")
                    exit()
                print("\nEmail is not correct")
                continue

    def get_custname(self):
            return self.name

    def set_custname(self, name):
            self.name = name

