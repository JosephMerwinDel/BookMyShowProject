import csv
import pandas as pd
import os

class csv_connection:

    global user_data_path
    user_data_path= r'src/data/UserData.csv'
    global movies_data_path
    movies_data_path= r'src/data/Movies.csv'
    def register_custdata_into_csv(list):
        assert os.path.isfile(user_data_path)
        with open(user_data_path, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(list)

    def write_moviedata_into_csv(list):
        with open(movies_data_path, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(list)

    def get_available_movies(self):
        dataframe = pd.read_csv(movies_data_path, usecols=['Title', 'Capacity', 'Genre', 'Length', 'Cast', 'Director', 'Admin Rating', 'Schedule', 'isDeleted'])
        count , no = 0, 0
        dict = {}
        for movie_details in dataframe.values.tolist():
            #print(title[6])
            list =[]

            if(int(movie_details[6]) > 0 and int(movie_details[8]) != 1):
                no +=1
                list.extend((movie_details[0], movie_details[1], movie_details[2], movie_details[3], movie_details[4], movie_details[5], movie_details[6], movie_details[7], count))
                print(str(no),".",movie_details[0])
            if(len(list)!= 0):
                count += 1
                dict[count] = list
        return dict

    def select_movie_from_table(self):
        dataframe = pd.read_csv(movies_data_path, usecols=['No.', 'Title', 'Capacity'])
        dataframe.iloc()

    def get_username_password(self):
        dict_username_password = {}
        dataframe = pd.read_csv(user_data_path, usecols=['Name', 'Password'])
        for username, password in dataframe.values.tolist():
            dict_username_password[username] = password
        return dict_username_password
