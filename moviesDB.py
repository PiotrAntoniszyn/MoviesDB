import sqlite3
import pickle
import hashlib
from movie import Movie
from person import Person
from award import Award
from cast import Cast
from ratin import Rating
conn = sqlite3.connect('movies.db')
c = conn.cursor()
c.execute("PRAGMA foreign_keys = 1")

#Metoda odpowiedzialna za proces logowania

# def save_obj(name, obj ):
#     with open('obj/'+ name + '.pkl', 'wb+') as f:
#         pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
#
# def load_obj(name ):
#     with open('obj/' + name + '.pkl', 'rb') as f:
#         return pickle.load(f)
#
# def logOn():
#     ifAdmin = input('Czy logowanie jako administrator? Y/N')
#     #if (ifAdmin == 'y' or  ifAdmin == 'Y'):
#
#     userLogin = input('Podaj login: ')
#     userPass = input('Podaj hasło: ')
#     if (userLogin not in logData.keys() or userPass not in logData.values()):
#         print('Błędny login lub hasło, spróbuj ponownie.')
#         logOn()
#     for key in logData:
#         if (userLogin == key and userPass == logData[key]):
#             print('Zalogowano. Witaj ' + str(userLogin))
#
#
# #Tworzenie nowego użytkownika
#
# def createUser():
#     userLogin = input('Podaj login: ')
#     userPass = input('Podaj hasło: ')
#     userRepeat = input('Powtórz hasło: ')
#     if(userLogin in logData.keys()):
#         print('Podany login jest już zajęty, podaj inny login')
#         createUser()
#     elif(userPass!=userRepeat):
#         print('Podane hasła nie są identyczne, spróbuj ponownie')
#         createUser()
#     else:
#         print('Pomyślnie utworzono konto! Witaj w klubie, '+ userLogin + '!')
#         logData.update({userLogin:userPass})
#         #
#         #dodać część odpowiedzialną za aktualizację pliku z danymi użytkowników
#         #
def loginPrompt():
    userLogin = input('Podaj login: ')
    userPass = (input('Podaj haslo: '))
    return (userLogin,userPass)

def logIn():
    sqlCreateTableQuery = 'CREATE TABLE IF NOT EXISTS Users (ID INTEGER PRIMARY KEY AUTOINCREMENT, Username TEXT, Password TEXT, IfAdmin BOOLEAN)'
    print("database created")
    c.execute(sqlCreateTableQuery)


    userCredentials = loginPrompt()

    sqlFindUserQuery  ="SELECT Username,Password,IfAdmin from Users WHERE Username LIKE '{login}'".format(login = userCredentials[0])

    c.execute(sqlFindUserQuery)
    queryResult = c.fetchall()


    if len(queryResult)==0:
        createUser(userCredentials[0],userCredentials[1])
        print("Utworzono konto")
        logIn()

    elif len(queryResult)==1:
        login_success = False
        while login_success ==  False:
            #moze sie wydawac niepotrzebne, ale jesli tam nizej przy blednym loginie/hasle zmieni sie nie tylko haslo, ale tez login, to bez tego ni pojdzie (chyba xD)
            sqlFindUserQuery = "SELECT Username,Password,IfAdmin from Users WHERE Username LIKE '{login}'".format(login=userCredentials[0])
            c.execute(sqlFindUserQuery)
            if userCredentials[1] == c.fetchone()[1]:
                print('Zalogowano. Witaj {user}'.format(user=userCredentials[0]))

                return userCredentials[0]

            else:
                print('Bledny login lub haslo, sprobuj ponownie.')
                userCredentials = loginPrompt()

#Tworzenie nowego użytkownika

def createUser(userLogin, userPassword):
    sqlAddUserQuery = "INSERT INTO Users (Username, Password, IfAdmin) VALUES ('{login}','{password}','{admin}')".format(
        login=userLogin,
        password=userPassword,
        admin=False)
    c.execute(sqlAddUserQuery)

def menu():
    checkIfAdmin =logIn()
    c.execute("SELECT IfAdmin from Users WHERE Username LIKE '{login}'".format(login=checkIfAdmin))
    d=c.fetchone()[0]
    if(d=='True'):
        print ("""
        1.Wyswietl Baze Filmow.
        2.Dodaj Film.
        3.Edytuj Film.
        4.Edytuj Uzytkownika
        """)
        ans=input("Co Chcesz zrobi")
        if ans=="1":
            print("\n BAZA FILMOW")
            browseMovies()
        elif ans=="2":
            print("\n DODAWANIE FILMOW")
            Create_new_movie()
        elif ans=="3":
            print("\n EDYCJA FILMOW")
            Edit_movie()
        elif ans=="4":
            print("\n EDYCJA UZYTKOWNIKA")

        else:
            print("\n Not Valid Choice Try again")
    else:
        print ("""
        1.Wyswietl Baze Filmow.
        2.Ocen film.
        """)
        ans=input("Co Chcesz zrobic")
        if ans=="1":
            print("\n Student Added")
        elif ans=="2":
            print("\n Student Deleted")
        elif ans !="":
            print("\n Not Valid Choice Try again")

def Create_new_movie():
    title = input("Title: ")
    genre = input("Genre: ")
    year = input("Year: ")
    x = Movie(None,title,genre,year)   #tworzenie obiektu klasy movie
    c.execute("INSERT INTO movie VALUES(:movie_id,:title,:genre,:year,null)" , {'movie_id': x.movie_id, 'title':x.title,
    'genre': x.genre, 'year':x.year})
    # directorName = input("Imie rezysera: ")
    # directorSurname = input("Nazwisko rezysera: ")
    # c.execute("SELECT first_name,last_name FROM person")
    # inBase=False
    # d=None
    # for first_name, last_name in c:
    #     if(directorName ==first_name and directorSurname==last_name):
    #         c.execute("INSERT INTO cast (cast_id,movie_id,person_id,if_actor) VALUES(:cast_id,:movie_id,(SELECT person_id FROM person WHERE first_name = directorName AND last_name = directorSurname ),0)" , {'cast_id': d,'movie_id': x.movie_id})
    #         inBase = True
    # if (inBase == False):
    #     p = Person(None,directorName,directorSurname,'Rezyser') #tworzenie obiektu klasy movie
    #     c.execute("INSERT INTO person VALUES(:person_id,:first_name,:last_name,:role)" ,
    #     {'person_id': p.person_id, 'first_name':p.first_name, 'last_name': p.last_name, 'role':p.role})
    #     c.execute("INSERT INTO cast (cast_id,movie_id,person_id,if_actor) VALUES(:cast_id,:movie_id,(SELECT person_id FROM person WHERE first_name =:directorName AND last_name =:directorSurname),0)" , {'cast_id': d,'movie_id': x.movie_id,'directorName':directorName,'directorSurname':directorSurname})
    #
def Create_new_cast():
    movie_id = input("Movie_Id: ")
    person_id = input("Person_Id: ")
    if_actor = input("If_Actor: ")
    x = Cast(None,movie_id,person_id,if_actor)   #tworzenie obiektu klasy movie
    c.execute("INSERT INTO cast VALUES(:cast_id,:movie_id,:person_id,:if_actor)" , {'cast_id': x.cast_id, 'movie_id': x.movie_id, 'person_id':x.person_id,
     'if_actor':x.if_actor})

def Create_new_award():
    while True:
        try:
            award_name = input("Nazwa nagrody: ")
            award_weight = input("Waga nagrody (od 1 do 5): ")
            person_id = input("Id osoby otrzymującej nagrode: ")
            x= Award(award_name,award_weight,person_id)
            c.execute("INSERT INTO award VALUES(:award_name,:award_weight,:person_id)" , {'award_name': x.award_name, 'award_weight': x.award_weight, 'person_id':x.person_id})
            break
        except sqlite3.IntegrityError:
            print ("Nie ma takiej osoby, sprobuj ponownie")
            Create_new_award()
def Edit_movie():
    Id_filmu = input("Podaj Id_filmu: ")
    print ("""
    1. Edytuj gatunek
    2. Edytuj rok
    3. Edytuj tytul
    4. Usun film
    """)
    ans=input("Co Chcesz zrobic")
    if ans=="1":
        genre = input("Podaj nowy gatunek: ")
        c.execute("UPDATE movie SET genre =? WHERE movie_id=? ",(genre,Id_filmu,))
        print("Zrobione")
    elif ans=="2":
        Year = input("Podaj nowy rok: ")
        c.execute("UPDATE movie SET Year =? WHERE movie_id=? ",(Year,Id_filmu,))
        print("Zrobione")
    elif ans=="3":
        title = input("Podaj nowy tytul: ")
        c.execute("UPDATE movie SET Title =? WHERE movie_id=? ",(title,Id_filmu,))
        print("Zrobione")
    elif ans=="4":
        c.execute("DELETE FROM movie WHERE movie_id=? ",(Id_filmu))
    elif ans !="":
        print("\n Not Valid Choice Try again")


def browseMovies():
    print ("""
    1. Przegladaj wszystkie
    2. Przegladaj pod katem gatunku
    3. Przegladaj pod katem roku
    4. Znajdz film
    """)
    ans=input("Co Chcesz zrobic")
    if ans=="1":
        c.execute("SELECT * FROM movie")
        rows = c.fetchall()
        for row in rows:
            print(row)
        #print("\n Student Added")
    elif ans=="2":
        print ("""
        1. Komedia
        2. Dramat
        3. Sensacja
        4. Bajka
        """)
        genreSort = input("Jaki gatunek wyswietlic?")
        if genreSort=="1":
            c.execute("SELECT * FROM movie WHERE genre LIKE 'komedia'")
            rows = c.fetchall()
            for row in rows:
                print(row)
        elif genreSort=="2":
            c.execute("SELECT * FROM movie WHERE genre LIKE 'dramat'")
            rows = c.fetchall()
            for row in rows:
                print(row)
        elif genreSort=="3":
            c.execute("SELECT * FROM movie WHERE genre LIKE 'sensacja'")
            rows = c.fetchall()
            for row in rows:
                print(row)
        elif genreSort=="4":
            c.execute("SELECT * FROM movie WHERE genre LIKE 'fantasy'")
            rows = c.fetchall()
            for row in rows:
                print(row)
        elif ans !="":
          print("\n Not Valid Choice Try again")

    elif ans=="3":
        uYear = input("Podaj rok: ")
        c.execute("SELECT * FROM movie WHERE year=?",(uYear,))
        rows = c.fetchall()
        for row in rows:
            print(row)
    elif ans=="4":
        uTitle = input("Podaj tytul filmu: ")
        c.execute("SELECT * FROM movie WHERE title=?",(uTitle,))
        rows = c.fetchall()
        for row in rows:
            print(row)

        print("\n Goodbye")
    elif ans !="":
        print("\n Not Valid Choice Try again")
def Create_new_person():
     first_name = input("First name: ")
     last_name = input("Last name: ")
     role = input("Role: ")
     x = Person(None,first_name,last_name,role) #tworzenie obiektu klasy movie
     c.execute("INSERT INTO person VALUES(:person_id,:first_name,:last_name,:role)" , {'person_id': x.person_id, 'first_name':x.first_name, 'last_name': x.last_name, 'role':x.role})


menu()
conn.commit()

conn.close()
