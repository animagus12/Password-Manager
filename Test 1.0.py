from tkinter import *
from PIL import ImageTk, Image
import mysql.connector
import random
import array

main = Tk()
main.title('Home')
main.geometry('400x400')

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="admin",
    database="password",
)

# Check to see if connection to MySQL was created
# print(mydb)

# Create a Cursor and initialize it
cur = mydb.cursor()

# Create a Database
# cur.execute("CREATE DATABASE password")

# Test to see if Database was created
# cur.execute("SHOW DATABASES")
# for db in cur:
#     print(db)

# Create a Table
cur.execute("CREATE TABLE IF NOT EXISTS pass(\
    username VARCHAR(255), \
    password VARCHAR(255), \
    site VARCHAR(255), \
    user_id INT AUTO_INCREMENT PRIMARY KEY)")

# Show Table
# p = cur.execute("SELECT * FROM pass WHERE user_id = 2")
# print(cur.description)

# for thing in cur.description:
#     print(thing)

def password_generator():
    password_box.delete(0, END)
    # maximum length of password needed
    MAX_LEN = 12

    # declare arrays of the character that we need in out password
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']

    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                        'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']

    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
            '*', '(', ')', '<']

    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS

    # randomly select at least one character from each character set above
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)

    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)

        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)

    password = ""
    for x in temp_pass_list:
            password = password + x
            
    password_box.insert(0, password)

def list_all():
    # Query the Database
    cur.execute("SELECT * FROM pass")
    result = cur.fetchall()

    for index, x in enumerate(result):
        num = 0
        for y in x:
            lookup_label = Label(main, text=y)
            lookup_label.grid(row=index + 7, column=num)
            num += 1

def clear():
    site_box.delete(0, END)
    username_box.delete(0, END)
    password_box.delete(0, END)
    
def add_to_db():
    sql_command = "INSERT INTO pass (username, password, site) VALUES (%s, %s, %s)"
    values = (username_box.get(), password_box.get(), site_box.get())
    cur.execute(sql_command, values)

    # Commit the changes to the database
    mydb.commit()
    # Clear all Field after Adding in Database
    clear()

def edit_db():
    edit = Tk()
    edit.title('Edit')
    edit.geometry('400x400')

    def changes():
        sql_command = """UPDATE pass SET username = %s, password = %s, site = %s WHERE user_id = %s"""
            
        user_name = username_box2.get()
        password = password_box2.get()
        site = site_box2.get()
        id_value = id_box2.get()

        input = (user_name, password, site, id_value)
        cur.execute(sql_command, input)

        mydb.commit()

        edit.destroy()

    sql2 = "SELECT * from pass WHERE user_id = %s"
    name2 = (edit_db_box.get(), )
    print (name2)
    results = cur.execute(sql2, name2)
    results = cur.fetchall()
    print(results)
                
    global site_box2
    site_box2 = Entry(edit)
    site_box2.grid(row= 1, column= 1)
    site_box2.insert(0, results[0][2])

    global username_box2
    username_box2 = Entry(edit)
    username_box2.grid(row= 2, column= 1)
    username_box2.insert(0, results[0][0])

    global password_box2
    password_box2 = Entry(edit)
    password_box2.grid(row= 3, column= 1)
    password_box2.insert(0, results[0][1])

    global id_box2
    id_box2 = Entry(edit)
    id_box2.grid(row= 4, column= 1)
    id_box2.insert(0, results[0][3])

    site_label = Label(edit, text= "Site Name")
    site_label.grid(row= 1, column= 0)

    username_label = Label(edit, text= "User name")
    username_label.grid(row= 2, column= 0)

    password_label = Label(edit, text= "password")
    password_label.grid(row= 3, column= 0)

    id_label = Label(edit, text= "User ID")
    id_label.grid(row= 4, column= 0)

    save_button = Button(edit, text= "Save all Changes", command= changes)
    save_button.grid(row= 5, column= 0, columnspan= 2)

def delete_db():
    delete_command = "DELETE FROM pass WHERE user_id = %s"
    item = (delete_from_db_box.get(), )
    cur.execute(delete_command, item)

    # Commit the changes to the database
    mydb.commit()
    # Clear all Field after Adding in Database
    clear()

def add_password():
    global site_box
    site_box = Entry(main)
    site_box.grid(row= 1, column= 1)

    global username_box
    username_box = Entry(main)
    username_box.grid(row= 2, column= 1)

    global password_box
    password_box = Entry(main)
    password_box.grid(row= 3, column= 1)

    global delete_from_db_box
    delete_from_db_box = Entry(main)
    delete_from_db_box.grid(row= 6, column= 0)

    global edit_db_box
    edit_db_box = Entry(main)
    edit_db_box.grid(row= 5, column= 0)

    site_label = Label(main, text= "Site Name")
    site_label.grid(row= 1, column= 0)

    username_label = Label(main, text= "User name")
    username_label.grid(row= 2, column= 0)

    password_label = Label(main, text= "password")
    password_label.grid(row= 3, column= 0)

    save_button = Button(main, text= "Add", command= add_to_db)
    save_button.grid(row= 4, column= 0)

    edit_button = Button(main, text= "Modify", command= edit_db)
    edit_button.grid(row= 5, column= 1)

    delete_button = Button(main, text= "Delete", command= delete_db)
    delete_button.grid(row= 6, column= 1)

    list_button = Button(main, text= "Show Entries", command= list_all)
    list_button.grid(row= 4, column= 1)

    generate_button = Button(main, text= "Generate Password", command= password_generator)
    generate_button.grid(row= 3, column= 2)
    
add_button = Button(main, text= "+", font= ("Helvetica", 24), command= add_password)
add_button.grid(row= 0, column= 0)


main.mainloop()