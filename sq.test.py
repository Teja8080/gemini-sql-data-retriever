import sqlite3
connection = sqlite3.connect('employee1.db')
cursor = connection.cursor()

data=cursor.execute("SELECT * FROM Naresh_it")
for row in data:
    print(row)