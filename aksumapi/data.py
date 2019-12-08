import sqlite3

# initialize a connection 
connection = sqlite3.connect('data.db')

# selects and executes and store the result
cursor = connection.cursor()

# create table. Name of table and columns in the table. 
# Use "INTEGER PRIMARY KEY" instead of good ole "int" if you want to create autoincrementing ids
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table2 = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table2)

# insert into the table
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
insert_query2 = "INSERT INTO items VALUES (?, ?)"

# commit & save data
connection.commit()

# close the connection
connection.close()


