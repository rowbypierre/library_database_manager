import psycopg2 # library work with Postgresql DB
# config function from created (local) config module
from config import config

# connection function
def connect():
    # connection object
    conn = None
    try:
        # read connection parameters from db ini
        params = config()
        
        # connect to PostgreSQL server
        print("")
        print('Attempting to connect to PostgreSQL "library" database...')
        conn = psycopg2.connect(**params)

        # cursor interact with databaase
        cur = conn.cursor()
        
        # execute statement 
        print("")
        print('PostgresSQL database version: ')
        cur.execute('select version();')
        
        # fetch results
        db_version = cur.fetchone()
        print("")
        print (db_version)
        
        # close Postgres communication
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("")
            print('Database connection closed.')
            
if __name__ == '__main__':
    connect()
        
        
        
        
