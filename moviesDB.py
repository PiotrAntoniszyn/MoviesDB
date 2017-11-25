import sqlite3
from movie import Movie
from person import Person
conn = sqlite3.connect('movies.db')
c = conn.cursor()
c.execute("PRAGMA foreign_keys = 1")
# c.execute("""CREATE TABLE movie(
#            movie_id integer primary key,
#            title text,
#            genre text,
#            year integer,
#            rating real,
#            unique(movie_id)
#
#            )""")
#
# c.execute("""CREATE TABLE person(
#            person_id integer primary key,
#            movie_id integer,
#            first_name text,
#            last_name text,
#            role text,
#            foreign key(movie_id) REFERENCES movie(movie_id),
#            unique(person_id)
#            )""")
#
# c.execute("""CREATE TABLE award(
#            award_name text primary key,
#            award_weight integer,
#            person_id integer,
#            foreign key(person_id) REFERENCES person(person_id),
#            unique(award_name)
#            )""")
#
# c.execute("""CREATE TABLE rating(
#            rating_id integer primary key,
#            movie_id integer,
#            person_id integer,
#            rate real,
#            foreign key(movie_id) REFERENCES movie(movie_id),
#            foreign key(person_id) REFERENCES person(person_id),
#            unique(rating_id)
#            )""")
# c.execute("""CREATE TABLE cast(
#            cast_id integer primary key,
#            movie_id integer,
#            person_id integer,
#            if_actor boolean,
#            foreign key(movie_id) REFERENCES movie(movie_id),
#            foreign key(person_id) REFERENCES person(person_id),
#            unique(cast_id)
#            )""")
# title = input("Title: ")
# genre = input("Genre: ")
# year = input("Year: ")
def Create_new_movie():
    title = input("Title: ")
    genre = input("Genre: ")
    year = input("Year: ")
    x = Movie(None,title,genre,year)   #tworzenie obiektu klasy movie
    c.execute("INSERT INTO movie VALUES(:movie_id,:title,:genre,:year, None)" , {'movie_id': x.movie_id, 'title':x.title, 'genre': x.genre, 'year':x.year})
# def Create_new_person():
#     first_name = input("First name: ")
#     last_name = input("Last name: ")
#     role = input("Role: ")
#     titleX = input("Title: ")
#     x = Person(None,first_name,last_name,role) #tworzenie obiektu klasy movie
#     c.execute("INSERT INTO person VALUES(:person_id,(SELECT movie_id from movie WHERE title = titleX),:first_name,:last_name,:role)" , {'person_id': x.person_id, 'first_name':x.first_name, 'last_name': x.last_name, 'role':x.role})


conn.commit()

conn.close()
