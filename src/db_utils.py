import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
    ALTER TABLE usuario
    ADD COLUMN token VARCHAR
''')
cursor.execute('''
    ALTER TABLE usuario
 ADD COLUMN blocked BOOLEAN DEFAULT 0
''')
cursor.execute('''
    ALTER TABLE usuario
    ADD COLUMN attempts INTEGER DEFAULT 0
''')

conn.close()

