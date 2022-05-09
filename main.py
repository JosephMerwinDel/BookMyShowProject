from src.Home import *
from src.Login import *

if __name__ == '__main__':
    login = Login()
    csv_con_obj = csv_connection()
    home = Home(login, csv_con_obj)
    home.select_options()

