import pyodbc

username = 'sa'
password = '123'
conn = pyodbc.connect(
    'Driver={ODBC Driver 17 for SQL Server}; Server=LAPTOP-266LSHVI; Database=QLSV; UID=' + username + '; PWD=' + password)

cursor = conn.cursor()

cursor.execute(
    f"insert into Student (name, email, phone) values(N'Kho', 'kho@gmail.com', '1232')")

cursor.commit()

for a in cursor.execute("select* from student"):
    print(a)
