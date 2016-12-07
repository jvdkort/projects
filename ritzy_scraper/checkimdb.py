
# coding: utf-8

# In[1]:

import sendgrid 
import os
from sendgrid.helpers.mail import *
import smtplib
import sys
from imdbpie import Imdb


TEMP_FILE_NAME = 'movies.json'
CURRENT_YEAR = '2016'
MINIMUM_RATING = 7.5


def filter_movie_names(movie_names):
    movie_names = list(set(movie_names)) # Get rid of duplicates
    filter_terms = {'Filter Events'}     # Filter movies title terms
    
    return [movie for movie in movie_names for tag in filter_terms if tag not in movie]


def extract_movie_names(json_file_name):
    """
        Extract movie names from the json file name provided.
    """
    with open(json_file_name, 'r') as in_file:
        json_file = json.loads(in_file.read())
        movie_names = [entry['name'] for entry in json_file]
        filtered_movie_names = filter_movie_names(movie_names)
        return filtered_movie_names


def imdb_movie_generator(imdb, movie_names):
    for movie_name in movie_names:
        for imdb_title in imdb.search_for_title(movie_name):
            if imdb_title['year'] == CURRENT_YEAR:
                imdb_title = imdb.get_title_by_id(imdb_title['imdb_id'])
                if imdb_title.rating and imdb_title.rating >= MINIMUM_RATING:
                    print("Found : {}".format(imdb_title.title))
                    yield imdb_title
                break
    print("Done!")
                    
                    
def send_email(movies):
    gmail_user = "example@gmail.com"
    gmail_pwd = "examplepassword"
    FROM = "noreplyexample@gmail.com"
    TO = ["example@gmail.com"]
    SUBJECT = "Highly rated movies of the day"
    TEXT = "High rated today:\n\n"
    for movie in movies:
        TEXT += 'Title: {} | Rating: {}\n'.format(movie.title, movie.rating)
        
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    # SMTP_SSL Example
    server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server_ssl.ehlo() 
    server_ssl.login(gmail_user, gmail_pwd)  
    server_ssl.sendmail(FROM, TO, message)
    server_ssl.close()
    
    print("successfully sent the mail")
  

if __name__ == '__main__':
    imdb = Imdb(anonymize=True)
    
    try:
        movie_names = extract_movie_names(sys.argv[1])
    except:
        movie_names = extract_movie_names('movie.json')
    
    movies = imdb_movie_generator(imdb, movie_names)
    
    send_email(movies)

