import sqlite3

def create_database():
    print('Creating database')
    db = sqlite3.connect('database\\main.db')
    cursor = db.cursor()

    print('Creating tables')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cfg_app_configuration
    (
        id TEXT PRIMARY KEY,
        value TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )           
    ''')

    print('Inserting data')    
    cursor.execute('''INSERT INTO cfg_app_configuration(id, value) 
                   VALUES('PARAM_1', 'VALUE_1')
                   ON CONFLICT(id) DO NOTHING''')

    print('Committing changes')
    db.commit()

    print('Closing connection')
    cursor.close()
    db.close()


def get_app_config():
    db = sqlite3.connect('database\\main.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()

    cursor.execute('SELECT * FROM cfg_app_configuration')

    rows = cursor.fetchall()

    result = [dict(row) for row in rows]

    cursor.close()
    db.close()

    return result


def add_app_config(id, value):
    db = sqlite3.connect('database\\main.db')
    cursor = db.cursor()
   
    cursor.execute(f'''INSERT INTO cfg_app_configuration(id, value) 
                   VALUES('{id}', '{value}')
                   ON CONFLICT(id) DO NOTHING''')

    db.commit()    
    cursor.close()
    db.close()