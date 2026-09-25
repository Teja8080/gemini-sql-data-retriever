import sqlite3
connection = sqlite3.connect('employee1.db')
cursor = connection.cursor()

table_info="""
Create table Naresh_it(employee_name varchar(30),
                       employee_role varchar(30), 
                       employee_salary FLOAT);
"""
cursor.execute(table_info)

cursor.execute("INSERT INTO Naresh_it VALUES('omkar nallagoni', 'data science', 75000)")
cursor.execute("INSERT INTO Naresh_it VALUES('teja', 'junior data science', 60000)")
cursor.execute("INSERT INTO Naresh_it VALUES('sai', 'python developer', 40000)")
cursor.execute("INSERT INTO Naresh_it VALUES('jaya vardhan', 'junior analyst', 65000)")
cursor.execute("INSERT INTO Naresh_it VALUES('mani', 'business analyst', 65000)")
cursor.execute("INSERT INTO Naresh_it VALUES('kiran', 'UI Developer', 75000)")
connection.commit()
connection.close()