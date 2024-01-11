import sys 
import psycopg2
from config import config

def logon():
    status = "locked" 
    uthreshold = 0
    pthreshold = 0

    while status == "locked":
        
        print("")
        username = input("Enter username: ").lower().strip()
        uthreshold += 1
    
        if uthreshold == 9:
            print("")
            print("Last attempt before script terminates.")
        elif (uthreshold == 10) and (username != "test"):
            print("")
            print("Terminating script...")
            sys.exit()
        elif username == "test":
            print("")
            print(f"Welcome {username}")
        
            while status == "locked":
                
                print("")
                password = input("Enter password: ").lower().strip()
                pthreshold += 1
            
                if (pthreshold == 9):
                    print("")
                    print("Last attempt before script terminates.")
                elif pthreshold == 10 and (password != "password"):
                    print("")
                    print("Terminating script...")
                    sys.exit()
                elif password == "password":
                    print("")
                    print(f"Correct password entered for username: {username}")
                    status = "unlocked"

if __name__ == '__main__':
    logon()
    
    parms = config()
    
    print("")
    print ('Attempting to establish connection to server: "localhost" database: "library" ...')
    
    conn = psycopg2.connect(**parms)
    cur = conn.cursor()
    
    print("")
    print("PostgreSQL database version: ")
    
    cur.execute('select version();')
    db_version = cur.fetchone()
    print("")
    print(db_version)
    
    print("""
Library Database Management System Utility
    
Operations include:
    1. Query table
    2. Update record(s)
    3. Insert record(s)
    4. Delete record(s)""")

    operation = input("Enter operation: ")
        
    if operation.isdigit() == False:
        print("")
        print("Enter numeric value 1, 2, 3, or 4")
        
        print("")
        print("Closing connection...")
        cur.close()
    else:
        while operation.isdigit() == True:
            
            if int(operation) > 4 or int(operation) < 1:
                print("")
                print("Select between Option 1 (Query Table) or Option 2 (Update record)")
            elif int(operation) == 1:
                print("")
                print("You've selected 1. Query table")
                print("")
                print("Tables to query include: ")
                print("1. Library catalog")
                print("2. Catalog physical condition")
                print("3. Available books:")
                print("4. Shelf warmers:")
                print("5. Book checkout durations")
                print("6. Overdue returns")
                print("7. Book fines summary")
                print("")
                
                operation = input("Enter selection: ")
                
                if operation.isdigit() == True and int(operation) == 1:
                    query = ''' select 		title as "Book Title",
			                                fname as "Author First Name",
			                                lname as "Author Last Name",
			                                mi as "Author MI"
                                from 		book_authors  ba
			                                left join authors a on ba.author_id = a.id
			                                left join books b on ba.book_id = b.id 
			                                left join statuses s on b.status_id = s.id
                                where 		status in ('Available')
                                order by 	title, fname, lname;'''
                    print("")
                    print("Quering database...")
                    cur.execute(query)
                    resultset = cur.fetchall()
                    
                    print("")
                    print("Printing database result...")
                    print(resultset)
                    
                    print("")
                    print("Closing connection...")
                    cur.close()
                    
                
            elif int(operation) == 2:
                print("")
                print("You've selected 2. Update record(s)")
            elif int(operation) == 3:
                print("")
                print("You've selected 3. Insert record(s)")
            elif int(operation) == 4:
                print("")
                print("You've selected 4. Delete record(s)")






