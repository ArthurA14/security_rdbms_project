#############################################################################
import mysql.connector
from mysql.connector import connect, Error, errorcode
from getpass import getpass

import string
import random

from string import ascii_lowercase, digits
from tkinter import *
from tkinter.font import Font

#############################################################################
# Creating a new database connection and a new database
try:
    with connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
    ) as connection:
        create_db_query = "CREATE DATABASE IF NOT EXISTS securitydb"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
            print("DB creation is ok")
except Error as err:
    print("this database already exists.")
    

connection = mysql.connector.connect(host="localhost",
                                    user='root',
                                    password='',
                                    database="securitydb")

cursor = connection.cursor(buffered=True, dictionary=True) 


#############################################################################
# Creating a table using the 'CREATE TABLE' statement and filling of the table
def create_security_table():
    tablename = input("Enter table name: ")
    securitytable = """
    CREATE TABLE IF NOT EXISTS securitydb."""+tablename+"""(
    id INT NOT NULL, 
    username VARCHAR(30) DEFAULT NULL, 
    password VARCHAR(30) DEFAULT NULL
    )
    """
    try:
        print("Creating table {}: ".format(tablename), end='')
        with connection.cursor() as cursor:
            cursor.execute(securitytable)
            connection.commit()
    except Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("this table already exists.")
        else:
            print(err.msg)  

    # Filling of the table
    for k in range(0, 14): 
        try:
            print("Creating line {}: ".format('securityline'), end='')
            query = """
            INSERT INTO """+tablename+"""(id, username, password)
            VALUES
                (%s,%s,%s)
            """
            reference = (k, ''.join(random.choice(string.ascii_letters) for _ in range(6)), 
                            ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))) 
            with connection.cursor() as cursor:
                cursor.execute(query,reference)
                connection.commit()
        except Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK") 
        
create_security_table()


#############################===SQL INJECTION===###############################
###############################################################################

#get the username from the database
def getUser():
    username = usernameEntry.get()
    password = passwordEntry.get()
    with connection.cursor() as cursor:
        # without any protection against a sql injection
        request = f"SELECT username FROM users WHERE username = '{username}' and password = '{password}';"
        cursor.execute(request)

        # with a prepared query to prevent sql injection
        # request = f"SELECT username FROM users WHERE username = %(username)s and password = %(password)s;"
        # parameters = {'username': username, 'password': password}
        # cursor.execute(request, parameters)

        name = cursor.fetchall()
        connection.commit()
        if name == None:
            outputVar.set("Username or Password not valid")
        else:
            outputVar.set(f"Welcome {name[0]}")


##################################===GUI===##################################
#############################################################################

#color variables
black = "#101010"
gray = "#1a1a1a"
lightgray = "#999999"
white = "#ffffff"
pink = "#ff0066"
green = "#00ffaa"
purple = "#7b00ff"
back = gray
secondary = black
main = white
accent = pink

#create tkinter
root = Tk()

#change title, icon and background of the gui
root.title("SQL Injector")
root.resizable(False, False)
root.configure(bg=back)

#center the window on the screen
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
root.geometry(f"302x289+{(screenWidth//2)-(302//2)}+{(screenHeight//2)-(289//2)}")

#convert units to pixels
pixelVirtual = PhotoImage(width=1, height=1)

#add the nexa font
nexaBold = Font(family="Nexa-Bold", size=15)
nexaRegular = Font(family="Nexa-Regular", size=12)

#username
usernameLabel = Label(root, text="Username:", bg=back, fg=accent, font=nexaRegular).grid(row=0, column=0, padx=(40, 10), pady=(40, 10))

usernameEntry = Entry(root, width=10, bg=secondary, fg=main, borderwidth=0, insertbackground=main, font=nexaRegular)
usernameEntry.insert(END, "' or '' = '")
usernameEntry.grid(row=0, column=1, padx=(10, 40), pady=(40, 10))

#password
passwordLabel = Label(root, text="Password:", bg=back, fg=accent, font=nexaRegular).grid(row=1, column=0, padx=(40, 10), pady=(10, 15))

passwordEntry = Entry(root, width=10, bg=secondary, fg=main, borderwidth=0, insertbackground=main, font=nexaRegular)
passwordEntry.insert(END, "' or '1' = '1")
passwordEntry.grid(row=1, column=1, padx=(10, 40), pady=(10, 15))

#submit
submit = Button(root, text="Submit", command=getUser, image=pixelVirtual, compound="c", width=100, height=50, bg=secondary, fg=main, activebackground=back, activeforeground=main, borderwidth=0, font=nexaBold).grid(row=2, column=0, columnspan=2, pady=15)

#output text
outputVar = StringVar()
outputVar.set("Input a username and a password")
outputLabel = Label(root, textvariable=outputVar, bg=back, fg=main, font=nexaRegular)
outputLabel.grid(row=3, column=0, columnspan=2, pady=(15, 40))


#execute tkinter window
root.mainloop()

cursor.close()
cursor = connection.cursor(buffered=True, dictionary=True) 