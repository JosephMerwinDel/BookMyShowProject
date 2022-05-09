from Utilities.csv_connection import *
from datetime import datetime, timedelta
import ast

class Login:
    def __init__(self):
        pass

    def validate_login(self):
        print("\n****** Welcome to BookMyShow ******\n")
        no_Of_Attempts, count = 3, 0
        adminflag = False
        csv = csv_connection()
        dict = csv.get_username_password()
        for i in range(no_Of_Attempts):
            username = input("Enter Username: ")
            password = input("Enter Password: ")
            if username.lower() in dict.keys() and str(password) == str(dict[username]):
                if(username.lower() == 'admin'):
                    print("\n******Welcome Admin*******\n")
                    adminflag = True
                    adminlogin = AdminLogin()
                    adminlogin.select_options()
                else:
                    print("\n******Welcome {}******\n".format(username))
                    customerLogin = CustomerLogin()
                    customerLogin.select_movie()
                break
            elif username not in dict.keys() or str(password) != str(dict[username]):
                count += 1
                if(count == no_Of_Attempts):
                    print("Failed to Login, Program has exit!!")
                    exit()
                print("\nYour username or password is incorect, please try again !!!")
                continue

class AdminLogin(Login):

    def select_options(self):
        print("""Please choose the following options
1. Add New Movie Info
2. Edit Movie Info
3. Delete Movies 
4. Logout\n""")
        options = int(input("Enter: "))
        if(options == 1):
            print("\nPlease enter the movie details")
            self.add_new_movie()
        elif(options == 2):
            print("\nSelect movie which you want to edit:")
            csv = csv_connection()
            csv.get_available_movies()
        elif(options == 3):
            self.delete_movie()
            #Code imcomplete
            self.select_options()
        elif(options == 4):
            print("You are logged out")
            exit()

    def add_new_movie(self):
        list_of_movie_details = []
        title = input("Title: ")
        genre = input("Genre: ")
        length = self.validate_length()
        cast = input("Cast: ")
        director = input("Director: ")
        rating = input("Movie rating: ")
        language = input("language: ")
        no_of_shows = input("Number of Shows in a day: ")
        first_show_time = self.validate_first_show_time()
        interval_time = input("Interval Time (Please enter only in minutes): ")
        gap_between_shows = input("Gap Between Shows (Please enter only in minutes): ")
        capacity = input("Capacity: ")
        dict = self.calculate_time(length, no_of_shows, first_show_time, interval_time, gap_between_shows, capacity)
        list_of_movie_details.extend((title, genre, length, cast, director, rating, language, no_of_shows, first_show_time, interval_time
                                      , gap_between_shows, capacity, dict, 0))
        csv_connection.write_moviedata_into_csv(list_of_movie_details)
        print("\n****Movie Added****\n")
        self.select_options()

    def validate_length(self):
        first_show = input("Length (Enter time in HH:MM ): ")
        format = "%H:%M"
        try:
            res = bool(datetime.strptime(first_show, format))
        except ValueError:
            print("Please enter Length in the format 'HH:MM'")
            self.validate_length()
        return first_show

    def validate_first_show_time(self):
        length = input("First Show: (Enter time in HH:MM format):")
        format = "%H:%M"
        try:
            res = bool(datetime.strptime(length, format))
        except ValueError:
            print("Please enter first show in the format 'HH:MM' (hours:minutes)")
            self.validate_first_show_time()
        return length

    def calculate_time(self, length, no_of_shows, first_show_time, interval_time, gap_between_shows, capacity):
        dict = {}
        count = 0
        length_of_movie = length.split(':')
        interval_time_of_movie = int(interval_time)
        gap_bw_shws = int(gap_between_shows)
        date_and_time = datetime.strptime(first_show_time, '%H:%M')
        t1 = date_and_time.strftime("%I:%M %p")
        for i in range(int(no_of_shows)):
            list = []
            count += 1
            time_change = timedelta(hours=(int(length_of_movie[0])), minutes=int(length_of_movie[1]) + interval_time_of_movie)
            new_time = date_and_time + time_change
            t2 = new_time.time().strftime("%I:%M %p)")
            list.extend((t1, t2, capacity))
            t1 = (new_time + timedelta(minutes=gap_bw_shws)).time().strftime("%I:%M %p")
            t2 = ''
            date_and_time = date_and_time.strptime(t1[:5], '%H:%M')
            dict[count] = list
        return dict

    def delete_movie(self):
        csv = csv_connection()
        dict = csv.get_available_movies()
        if(len(dict) == 0):
            print("***No movies available***\n")
            self.select_options()
        else:
            print("\nPlease choose movie to delete\n")
            option = int(input("Enter:"))
            try:
                df = pd.read_csv('src/data/Movies.csv')
                for key,value in dict.items():
                    if(key == option):
                       # print(key, value[0])
                        df.loc[key, 'isDeleted'] = 1
                        df.to_csv("src/data/Movies.csv", index=False)
            except:
                print("Please select the correct option")
                self.delete_movie()
            print("\n****Movie Deleted succesfully****\n")
            self.select_options()

class CustomerLogin(Login):

    def select_movie(self):
        print("Please select the movie of your choice")
        csv = csv_connection()
        dict = csv.get_available_movies()
        movie_no = int(input("Enter movie:"))
        self.show_movie_details(movie_no, dict)


    def show_movie_details(self, movie_no_selected, movie_detail_dict):
        print("\n******Movie details*******\n")
        dict_movietimings = {}
        for movie_no, movie_detail in movie_detail_dict.items():
            if(movie_no == movie_no_selected):
                print('Title:', movie_detail[0])
                print('Genre:', movie_detail[1])
                print('Length:', movie_detail[2], 'hrs')
                print('Cast:', movie_detail[3])
                print('Director:', movie_detail[4])
                print('Admin Rating:', int(movie_detail[5]), '/10')
                print('Timings:')
                count = 0
                dict_timings = ast.literal_eval(movie_detail[7])
                for key, value in dict_timings.items():
                    count+= 1
                    print(count,'.',value[0], '-',value[1])
                self.select_timings(dict_timings)

    def select_timings(self, dict_timings):
        print('''Select Options:
1.Book Tickets 
2.Cancel Tickets
3.Give User Rating''')
        options = int(input('Enter: '))
        if(options ==1):
            print('\nTimings:')
            count = 0
            for key, value in dict_timings.items():
                count += 1
                print(count, '.', value[0], '-', value[1])
            option = int(input('Select Timings:'))
            for key, value in dict_timings.items():
                if(option == key):
                    print('Timing:', value[0], '-', value[1])
                    print('Remaining seats:', value[2])
            input('Enter Number of seats:')
            print('Thanks for booking.')
        elif(options == 2):
            print('\n******Welcome User1*******\n')
            no_of_seats_to_cancel = int(input('Number of seats you want to cancel:'))
        elif(options == 2):
            print('\n******Welcome User1*******\n')
            user_ratings = int(input('Please enter rating for the following movie:'))






