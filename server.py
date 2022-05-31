import mariadb 
import sys

conn = mariadb.connect(
    user="root",
    password="Arfarf123",
    host="localhost",
    database="tasklistingdb")

cur = conn.cursor() 

#retrieving information 
# some_name = "Georgi" 
# cur.execute("SELECT first_name,last_name FROM employees WHERE first_name=?", (some_name,)) 

# for first_name, last_name in cur: 
#     print(f"First name: {first_name}, Last name: {last_name}")
    
#insert information 
# try: 
#     cur.execute("INSERT INTO employees (first_name,last_name) VALUES (?, ?)", ("Maria","DB")) 
# except mariadb.Error as e: 
#     print(f"Error: {e}")

# conn.commit() 
# print(f"Last Inserted ID: {cur.lastrowid}")

# cur.execute("INSERT INTO user (user_id, username, password, email) VALUES(?,?,?,?)",(1,"zeke", "jaeger", "zjaeger@aot.ani.to",))

# for username in cur:
#     print(f"Username:{username}")
# conn.commit() 

# delete
# cur.execute("DELETE FROM user")
# conn.commit() 

# cur.execute("SELECT * FROM user")
# print(cur.fetchall())
# check connection to database
# cur.execute("SHOW DATABASES")

# for x in cur:
#     print(x)

# conn.commit()    
# conn.close()