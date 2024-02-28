import psycopg2
import sys
import os
from config import config
from login import logon
from datetime import datetime
import time

menuMessage = """
Library Database Management System Utility (LDMSU)
    
LDMSU functions:
    1. Read reports/ stored queries
    2. Update record
    3. Create record
    4. Delete record
    
Enter 'exit' to exit utility
"""
def menu():
    os.system("clear")
    print(menuMessage)
    time.sleep(1)

def ouput_dt_convert(resultset):
    for row in resultset:
        formatted_row = list(row)
        for i, item in enumerate(formatted_row):
            if isinstance(item, datetime):
                formatted_row[i] = item.strftime('%Y-%m-%d %H:%M:%S')
        print(tuple(formatted_row))
        time.sleep(.25)

if __name__ == '__main__':
    os.system("clear")
    logon()
    
    print()
    print('Connecting to server: "localhost" database: "library"')
    time.sleep(1)
    parms = config()
    conn = psycopg2.connect(**parms)
    cur = conn.cursor()
    
    def end():
        os.system("clear")
        print()
        print("Closing connection...")
        time.sleep(1)
        print()
        print("Exiting program...")
        time.sleep(1)
        cur.close()
        os.system("clear")
        sys.exit()
    
    print()
    print("Connection established...")
    time.sleep(1)
    os.system("clear")
    print()
    print("Querying database version...")
    print()
    time.sleep(1)
    cur.execute('select version();')
    db_version = cur.fetchone()
    db_version = str(db_version).replace("'","").replace(",","").replace(")","").replace("(","").strip()
    print(f"PostgreSQL version: {db_version}")
    time.sleep(1)
    menu()
    operation = input("Enter function #: ")
    time.sleep(.5)
    if operation == "exit":
        end()   
    elif operation.isdigit() == False:
        print()
        print("Numeric value not entered") 
        time.sleep(1)
        end()
    else:
        
        while operation.isdigit() == True:    
            if int(operation) > 4 or int(operation) < 1:
                menu()
                operation = input("Enter function #: ")
                time.sleep(.5)
                if operation == "exit":
                    end()                      
                elif operation.isdigit() == False:
                    end()
                
            elif int(operation) == 1:
                os.system("clear")
                print()
                print("Selection: 1. Execute query")
                time.sleep(.5)
                print()
                print("Queries include: ")
                print("1. Library catalog")
                print("2. Catalog physical condition")
                print("3. Available books")
                print("4. Shelf warmers")
                print("5. Book checkout durations")
                print("6. Overdue returns")
                print("7. Book fines summary")
                print("8. Monthly loans # (time series)")
                print("9. Patron Activity")
                print()
                
                qoperation = input("Enter # (1-7) for query: ")
                time.sleep(.5)
                if qoperation == "exit":
                    end()                                            
                elif qoperation.isdigit() == True and int(qoperation) == 1: 
                    os.system("clear")                   
                    print()
                    print("Querying database...")
                    time.sleep(1)
                    query = ''' 
                            select 		title "Title", isbn "ISBN", genre "Genre", condition "Condition"
                            from        books b
                                        left join genres g on g.id = b.genre_id  
                                        left join conditions c on c.id = b.condition_id                   
                                        left join statuses s on s.id = b.status_id                   
                            order by	Genre, Title;'''
                    
                    cur.execute(query)
                    resultset = cur.fetchall()
                    header = '(Title, ISBN, Genre, Book Condition)'
                    print()
                    print("Printing resultset...")
                    time.sleep(1)
                    os.system('clear')
                    print()
                    print(header)
                    print()                    
                    for row in resultset:
                        print(row)
                        time.sleep(.25) 
                    print()
                    print(header)
                    
                    print()    
                    print("Return to menu?")
                    time.sleep(.5)
                    print()
                    coa = input("Enter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.5)
                    if coa[0] == 'y':
                        menu()
                        options = [1, 2, 3, 4]
                        operation = input("Enter function #: ")
                        time.sleep(.5)
                        if operation == "exit":
                            end()                     
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end()
                        else:
                            pass
                            
                    if coa[0] != 'y':   
                        end()
                
                elif qoperation.isdigit() == True and int(qoperation) == 2:
                    os.system("clear")                    
                    print()
                    print("Querying database...")
                    time.sleep(1)
                    query = ''' 
                            select      condition "Condition",			
                                        count(*) "Count",			
                                        concat((count(*) * 100/(select count(*) from books)) , '% of Books') "Percent"
                            from		books b
                                		left join conditions c on c.id = b.condition_id        
                            group by 	condition
                            order by    "Count" desc, condition;'''
                    
                    cur.execute(query)
                    resultset = cur.fetchall()
                    header = '(Condition, Count, Percent)'
                    print()
                    print("Printing resultset...")
                    time.sleep(1)
                    os.system('clear')
                    print()
                    print(header)
                    print()                    
                    for row in resultset:
                        print(row)
                        time.sleep(.25)
                    print()
                    print(header)  
                      
                    print()
                    print("Return to menu?")
                    time.sleep(.5)
                    print()
                    coa = input("Enter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.5)
                    if coa[0] == 'y':
                        menu()
                        options = [1, 2, 3, 4]
                        operation = input("Enter function #: ")
                        time.sleep(.5)
                        if operation == "exit":
                            end()                     
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end()
                        else:
                            pass
                        
                    if coa[0] != 'y': 
                        end()
                    
                elif qoperation.isdigit() == True and int(qoperation) == 3:   
                    os.system("clear")                 
                    print()
                    print("Querying database...")
                    time.sleep(1)
                    query = ''' 
                            with x as (
                                select 		--*,
						                    title as "Book Title",
						                    concat(fname,' ', mi, '. ', lname) as "Full Name"
                                from 		book_authors  ba
						                    left join authors a on ba.author_id = a.id
						                    left join books b on ba.book_id = b.id 
						                    left join statuses s on b.status_id = s.id
                                where 		status in ('Available')
                                group by 	"Full Name", "Book Title"
                                order by 	"Book Title"
                                )
                                
                            select		x."Book Title",
                            		    string_agg("Full Name", ', ') as Author
                            from        x
                            group by    x."Book Title"
                            order by    x."Book Title";		
                            '''
                    cur.execute(query)
                    resultset = cur.fetchall()
                    header = '(Book Title, FName MI. LName)'
                    print()
                    print("Printing resultset...")
                    time.sleep(1)
                    os.system('clear')
                    print()
                    print(header)   
                    print()      
                    for row in resultset:
                        print(row)
                        time.sleep(.5)
                    print()
                    print(header)   
                    
                    print()
                    print("Return to menu?")
                    time.sleep(.5)
                    print()
                    coa = input("Enter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.5)
                    if coa[0] == 'y':
                        menu()
                        options = [1, 2, 3, 4]
                        operation = input("Enter function #: ")
                        time.sleep(.5)
                        if operation == "exit":
                            end()                    
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end()
                        else:
                            pass
                        
                    if coa[0] != 'y':   
                        end()
                    
                elif qoperation.isdigit() == True and int(qoperation) == 4:
                    os.system("clear")                    
                    print("Querying database...")
                    time.sleep(1)
                    query = ''' 
                            with x as (
                                select 		--*,
                                            title as "Book Title",
                                            concat(fname,' ', mi, '. ', lname) as "Full Name"
                                from 		book_authors  ba
                                            left join authors a on ba.author_id = a.id
                                            left join books b on ba.book_id = b.id 
                                            left join statuses s on b.status_id = s.id
                                where 		b.id not in (select book_id from loans)
                                order by 	"Book Title"
                            )

                            select		x."Book Title",
                                        string_agg("Full Name", ', ') as Author			
                            from 		x 
                            group by 	x."Book Title"
                            order by 	x."Book Title";'''
                    print()
                    cur.execute(query)
                    resultset = cur.fetchall()
                    header = '(Book Title, Author First Name, Author Last Name, Author MI)' 
                    print("Printing resultset...")
                    time.sleep(1)
                    os.system('clear')
                    print()
                    print(header)    
                    print()            
                    for row in resultset:
                        print(row)
                        time.sleep(.25)
                    print()
                    print(header)
                    
                    print()    
                    print("Return to menu?")
                    time.sleep(.5)
                    print()
                    coa = input("Enter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.5)
                    if coa[0] == 'y':
                        os.system("clear")
                        menu()
                        options = [1, 2, 3, 4]
                        operation = input("Enter function #: ")
                        time.sleep(.5)
                        if operation == "exit":
                            end()                     
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end()
                        else:
                            pass
                        
                    if coa[0] != 'y': 
                        end()
                    
                elif qoperation.isdigit() == True and int(qoperation) == 5:     
                    os.system("clear")  
                    print("Querying database...")
                    time.sleep(1)
                    query = ''' 
                            with x as (
	                            select		*,
				                            case when r.date is not null 
				                                then r.date 
				                                else current_date 
				                            end as "Return Date",
				                            case when c.date is not null 
				                                then c.date
				                                else current_date
				                            end as "Checkout Date"
	                            from		books b
				                            left join loans l  on b.id = l.book_id 
				                            left join returns r on r.id = l.return_id
				                            left join checkouts c on c.id = l.checkout_id
                            ) 

                            select 		title "Book Title",
			                            ("Return Date" - "Checkout Date") as "Days Loaned" 
                            from		x
                            order by	"Days Loaned" desc;'''
                    print()
                    cur.execute(query)
                    resultset = cur.fetchall()
                    print("Printing resultset...")
                    time.sleep(1)
                    os.system('clear')
                    print()
                    header = '(Book Title, Days Loaned)'
                    print(header)
                    print()                    
                    for row in resultset:
                        print(row)
                        time.sleep(.25)
                    print()
                    print(header)
                    
                    print()
                    print("Return to menu?")
                    time.sleep(.5)
                    print()
                    coa = input("Enter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.5)
                    if coa[0] == 'y':
                        os.system("clear")
                        menu()
                        options = [1, 2, 3, 4]
                        operation = input("Enter function #: ")
                        time.sleep(.5)
                        if operation == "exit":
                            end()                     
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end()
                        else:
                            pass
                        
                    if coa[0] != 'y': 
                        end()
                    
                elif qoperation.isdigit() == True and int(qoperation) == 6:     
                    os.system("clear")              
                    print("Querying database...")
                    time.sleep(1)
                    query = ''' 
                            with x as ( 
	                            select 	concat(p.fname, ' ', p.lname) as "Patron",
			                            b.title "Book",
			                            c.date "Checkout",
			                            l.due "Due",
			                            r.date "Returned",
			                            (r.date - l.due) "Days Overdue",
			                            concat('$',r.fine) "Fine"
	                            from 	loans l
			                            join checkouts c on c.id = l.checkout_id
			                            join returns r on r.id = l.return_id
			                            join books b on b.id = l.book_id
			                            join patrons p on p.id = l. patron_id
                                )

	                            select 		* 
	                            from 		x 
	                            where 		"Days Overdue" > 0
	                            order by	"Days Overdue" desc;'''

                    cur.execute(query)
                    resultset = cur.fetchall()
                    header = '(Patron, Book, Checkout, Due, Returned, Days Overdue, Fine)'
                    print()
                    print("Printing resultset...")
                    time.sleep(1)
                    os.system('clear')
                    print()
                    print(header)                    
                    print()
                    for row in resultset:
                        print(row)
                        time.sleep(.25)
                    print("")
                    print(header)
                    
                    print()
                    print("Return to menu?")
                    time.sleep(.5)
                    print()
                    coa = input("Enter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.5)
                    if coa[0] == 'y':
                        os.system("clear")
                        menu()
                        options = [1, 2, 3, 4]
                        operation = input("Enter function #: ")
                        time.sleep(.5)
                        if operation == "exit":
                            end()                     
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end()
                        else:
                            pass
                        
                    if coa[0] != 'y':  
                        end()
                    
                elif qoperation.isdigit() == True and int(qoperation) == 7:   
                    os.system("clear")               
                    print()
                    print("Querying database...")
                    time.sleep(1)
                    query = ''' 
                            with x as ( 
	                            select 	*,
			                            (r.date - l.due) "Days Overdue"
	                            from 	loans l
			                            join returns r on r.id = l.return_id
			                            join books b on b.id = l.book_id
			                            join genres g on g.id = b.genre_id
                            )

	                            select 		genre "Genre",
			                                concat('$', round(avg (fine), 2)) "Fine (AVG)"
	                            from 		x 
	                            where 		"Days Overdue" > 0
	                            group by	"Genre"
	                            order by	"Genre";'''
                    cur.execute(query)
                    resultset = cur.fetchall()
                    header = '(Genre, Fine (AVG))'
                    print()
                    print("Printing resultset...")
                    time.sleep(1)
                    os.system('clear')
                    print()
                    print(header)
                    print()                    
                    for row in resultset:
                        print(row)
                        time.sleep(.25)
                    print()
                    print(header)
                    
                    print()
                    print("Return to menu?")
                    time.sleep(.5)
                    print()
                    coa = input("Enter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.5)
                    if coa[0] == 'y':
                        os.system("clear")
                        menu()                       
                        options = [1, 2, 3, 4]
                        operation = input("Enter function #: ")
                        time.sleep(.5)
                        if operation == "exit":
                            end()                     
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end() 
                        else:
                            pass
                    
                    if coa[0] != 'y':
                        end()              
                
                elif qoperation.isdigit() == True and int(qoperation) == 8:   
                    os.system("clear")               
                    print()
                    print("Querying database...")
                    time.sleep(1)
                    query = ''' 
                            with x as (
                                select 	date_part('year', c.date) "Year", 
                                        date_part('month', c.date) "Month #", 
                                        to_char(c.date, 'Month') "Month",
                                        date_part('month', (c.date - interval '1 month')) "Previous Month #",
                                        count(*) as "Loans"
                                from 	loans
                                        join returns r on r.id = loans.return_id
                                        join checkouts c on c.id = loans.checkout_id
                                group by date_part('year', c.date), date_part('month', c.date), date_part('month', (c.date - interval '1 month')), to_char(c.date, 'Month')
                                order by	"Year", "Month #" desc
                            )

                            select 	  "Year"
                                    , "Month"
                                    , "Loans" as "# of Loans"
                                    , case
                                        when x2."Loans" - (select x."Loans" from x where x."Month #" = x2."Previous Month #") is null 
                                            then '0.00 %'
                                        else   
                                            concat(
                                                cast (((
                                                    round(((
                                                        cast(x2."Loans" - (select x."Loans" from x where x."Month #" = x2."Previous Month #") as numeric)) / x2."Loans"), 2) * 100)) as text), ' %')
                                        end as "Growth (Prev. Month)"
                            from	x as x2 
                            ; '''
                    cur.execute(query)
                    resultset = cur.fetchall()
                    header = '(Year, Month, # of Loans, Growth (Prev. Month))'
                    print()
                    print("Printing resultset...")
                    time.sleep(1)
                    os.system('clear')
                    print()
                    print(header)
                    print()                    
                    for row in resultset:
                        print(row)
                        time.sleep(.25)
                    print()
                    print(header)
                    
                    print()
                    print("Return to menu?")
                    time.sleep(.5)
                    print()
                    coa = input("Enter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.5)
                    if coa[0] == 'y':
                        os.system("clear")
                        menu()                       
                        options = [1, 2, 3, 4]
                        operation = input("Enter function #: ")
                        time.sleep(.5)
                        if operation == "exit":
                            end()                     
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end() 
                        else:
                            pass
                    
                    if coa[0] != 'y':
                        end()  
                
                elif qoperation.isdigit() == True and int(qoperation) == 9:   
                    os.system("clear")               
                    print()
                    print("Querying database...")
                    time.sleep(1)
                    query = ''' 
                            select 		l.patron_id "ID", concat(p.fname, ' ', p.lname) "Name"
                                        , round(avg(fine), 2) "Fines (AVG)"
                                        , count(comments_neg.id) "# Negative Comments"
                                        , count(comments_pos.id) "# Positive Comments"
                                        , count(overdue.id) "# Overdue Returns"
                                        , count(early_returns.id) "# Early Returns"
                                        , fav.genre "Favorite Genre"
                            from 		loans l
                                        left join patrons p on l.patron_id = p.id
                                        left join ( select 	fine, id from 	returns ) fines on fines.id = l.return_id
                                        left join ( select 	 id, comment
                                                    from 	returns 
                                                    where 	comment like '%late%'
                                                            or comment like '%damage%'
                                                            or comment like 'lost'
                                                            or comment like '%missing%' ) comments_neg  on comments_neg.id = l.return_id
                                        left join ( select 	id, comment
                                                    from 	returns 
                                                    where 	comment not like '%late%'
                                                            and comment not like '%damage%'
                                                            and comment not like '%lost%'
                                                            and comment not like '%missing%' ) comments_pos on comments_pos.id = l.return_id		
                                        left join ( select 	id, overdue from 	returns where 	overdue = true) overdue on overdue.id = l.return_id	
                                        left join ( select  id from returns where 	comment like '%early%' ) early_returns on early_returns.id = l.return_id	
                                        left join ( select 	patron_id, genre		
                                                    from		(select 	*, row_number() over(partition by patron_id, genre order by count desc) "copy"
                                                                from 		(select 	count(*) "count", patron_id, genre
                                                                            from 		loans l
                                                                                        join books b on b.id = l.book_id
                                                                                        join genres g on g.id = b.genre_id 	
                                                                            group by 	patron_id, genre) x) y
                                                    where 	copy = 1 )fav on fav.patron_id = l.patron_id				
                            group by  	l.patron_id, concat(p.fname, ' ', p.lname), fav.genre 
                            order by 	"Favorite Genre", "ID"; 
                            ; '''
                    cur.execute(query)
                    resultset = cur.fetchall()
                    header = '(ID, Name, Fines (AVG), # of Negative Comments, # of Positive Comments, Overdue Returns, # of Early Returns, Favorite Genre)'
                    print()
                    print("Printing resultset...")
                    time.sleep(1)
                    os.system('clear')
                    print()
                    print(header)
                    print()                    
                    for row in resultset:
                        print(row)
                        time.sleep(.25)
                    print()
                    print(header)
                    
                    print()
                    print("Return to menu?")
                    time.sleep(.5)
                    print()
                    coa = input("Enter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.5)
                    if coa[0] == 'y':
                        os.system("clear")
                        menu()                       
                        options = [1, 2, 3, 4]
                        operation = input("Enter function #: ")
                        time.sleep(.5)
                        if operation == "exit":
                            end()                     
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end() 
                        else:
                            pass
                    
                    if coa[0] != 'y':
                        end() 
                        
                else:                    
                    print("Enter numeric value between 1 - 9")
                    time.sleep(.5)
                                            
            elif int(operation) == 2:
                os.system("clear")
                print()
                print("Selection: 2. Update record")
                time.sleep(.5)
                print()
                print("Querying database tables...")
                query ="""
                select  --*,
                        table_name
                from    information_schema.tables
                where   table_catalog = 'library'
                        and table_schema = 'public'
                        and table_name not like '%book_authors%';
                """
                cur.execute(query)
                resultset = cur.fetchall()
                tables = []                    
                for row in resultset:
                    rowx = ''.join(row)
                    rowx = rowx.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                    tables.append(rowx)
                
                print()
                print("Printing tables:")
                time.sleep(1)
                print()
                for table in tables:
                    print(table)
                    time.sleep(.25)
                    
                print() 
                uoperation = input("Enter table: ")
                time.sleep(.5)
                if uoperation == "exit":
                    end()
                                                              
                elif uoperation.isdigit() == False and uoperation.lower() in tables:
                    os.system("clear")
                    print()
                    print("Querying database...")
                    time.sleep(1)
                    os.system("clear")
                    query = f"""
                    select  string_agg(column_name, ' , ') as column_string
                    from 	information_schema.columns
                    where 	table_name = '{uoperation.lower()}';
                    """
                    cur.execute(query)
                    resultset = cur.fetchall()
                    stringx = ""
                    resultset = str(resultset).split(",")
                    count = len(resultset)
                    counter = 0 
                    for x in resultset:
                        x = str(x)
                        x = x.replace(" ", "").replace("'", " ")
                        counter = counter +1
                        if counter != count and counter == count - 1:
                            stringx = stringx + x
                        elif counter != count and counter != count - 1:
                            stringx = stringx + x + " , "
                        elif counter == count:
                            stringx = stringx + x 
                    targetTemplate = stringx.replace("[", "").replace("]", "")    
                                               
                    query = f"select * from {uoperation.lower()};"
                    cur.execute(query)
                    resultset2 = cur.fetchall()
                    print(f"Printing '{uoperation}' table records:")
                    time.sleep(1)
                    print()
                    print(targetTemplate)
                    print()
                    ouput_dt_convert(resultset2)
                    time.sleep(.25)
                    print()
                    print(targetTemplate)
                        
                    print()
                    print("Unique identifier (id) from above required.")
                    time.sleep(.5)
                    print()
                    pkey = input("Enter id: ")
                    time.sleep(.5)
                    if pkey == "exit":
                        end()
                                                              
                    elif pkey.isdigit() == True and int(pkey) > 0:
                        
                        pkey = int(pkey)
                        targetQuery = f"""select * from {uoperation} where id = {pkey};"""
                        cur.execute(targetQuery)
                        targetRecord = cur.fetchall()
                        for row in targetRecord:
                            formatted_row = list(row)
                            for i, item in enumerate(formatted_row):
                                if isinstance(item, datetime):
                                    formatted_row[i] = item.strftime('%Y-%m-%d %H:%M:%S')
                            targetRecord = tuple(formatted_row)
                        
                        os.system("clear")
                        print()
                        print(f"Querying database, retrieving {uoperation} table definiton...")
                        time.sleep(1)
                        print()
                        print("Fields:")
                        time.sleep(.5)
                        print()
                        print("'data field' : 'datatype'")
                        query = f"""
                        select 	column_name, data_type
                        from 	information_schema.columns
                        where 	table_name = '{uoperation}';
                        """
                        cur.execute(query)
                        resultset = cur.fetchall()
                        datatypes = {}
                        columns = []
                        for column in resultset:
                            columnx = str(column)
                            columnx = columnx.strip().replace(')', '').replace('(', '').replace("'", "")
                            x = columnx.split(', ')
                            field = x[0]
                            datatype = x[1]
                            print(f"{field} : {datatype}")
                            time.sleep(.25)
                            datatypes.update({field : datatype})
                            columns.append(field)
                        
                        print()
                        print() 
                        print("Record: ")
                        time.sleep(.5)
                        print()
                        print(targetTemplate)
                        print(targetRecord)
                        time.sleep(.25)    
                        print()
                        attribute = input("Enter field to update: ")
                        time.sleep(.5)
                        attribute = attribute.strip().lower()
                        
                        if attribute in columns:
                            os.system("clear")
                            print()
                            print(f"{attribute.capitalize()} field has datatype: '{datatypes.get(attribute)}'")
                            
                            intFields = []
                            query = """
                                    select distinct 	column_name --, data_type 
                                    from 				information_schema."columns"
                                    where 				table_catalog = 'library'
                                                        and data_type in ('bigint', 'numeric', 'smallint', 'int', 'integer')
                                                        and table_name not like '%pg%'     
                            """
                            cur.execute(query)
                            resultset = cur.fetchall()
                            for fields in resultset:
                                fieldx = ''.join(fields)
                                fieldx = fieldx.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                                intFields.append(fieldx)
                            
                            dateFields = []
                            query = f"""
                                        select distinct 	column_name --, data_type 
                                        from 				information_schema."columns"
                                        where 				table_catalog = 'library'
                                                            and data_type like '%date%'
                                                            and table_name = '{uoperation}';   
                                    """
                            cur.execute(query)
                            resultset = cur.fetchall()
                            for fields in resultset:
                                fieldx = ''.join(fields)
                                fieldx = fieldx.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                                dateFields.append(fieldx)
                                
                            tsFields = []
                            query = f"""
                                        select distinct 	column_name --, data_type 
                                        from 				information_schema."columns"
                                        where 				table_catalog = 'library'
                                                            and data_type like'%timestamp%'
                                                            and table_name = '{uoperation}';   
                                    """
                            cur.execute(query)
                            resultset = cur.fetchall()
                            for fields in resultset:
                                fieldx = ''.join(fields)
                                fieldx = fieldx.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                                tsFields.append(fieldx)    
                            
                            print()
                            print(targetTemplate)
                            print(targetRecord)    
                            
                            if ((attribute not in tsFields) and (attribute not in dateFields)): 
                                print()
                                newValue = input(f"Enter new value for {attribute}: ")
                                time.sleep(.5)
                                if attribute not in intFields:
                                    newValue =  newValue.strip().replace("'", "''")
                                    newValue = "'" + newValue + "'"
                                elif attribute in intFields: 
                                    newValue = int(newValue)
                            elif attribute in dateFields:
                                print()     
                                newValue = input(f"Provide value formatted as 'YYYY-MM-DD' for field '{attribute}' : ")
                                time.sleep(.5)
                            elif attribute in tsFields:
                                print()
                                newValue = input(f"Provide value formatted as 'YYYY-MM-DD hh:mm:ss' for field '{attribute}' : ")
                                time.sleep(.5)
                                    
                            query =f"""
                                    update {uoperation}
                                    set {attribute} = {newValue}
                                    where id = {pkey};
                                    
                                    commit; """
                            cur.execute(query)
                            os.system("clear")
                            print()
                            print("Updating record...")
                            time.sleep(1) 
                            print()
                            # print(f"Database message: {resultset}")
                            print("Querying updated record...")
                            time.sleep(1)
                            os.system("clear")
                             
                            query = f"""select * from {uoperation} where id = {pkey};"""
                            cur.execute(query)
                            resultset = cur.fetchall()
                            for row in resultset:
                                formatted_row = list(row)
                                for i, item in enumerate(formatted_row):
                                    if isinstance(item, datetime):
                                        formatted_row[i] = item.strftime('%Y-%m-%d %H:%M:%S')
                                resultset = tuple(formatted_row)
                            print("Printing updated record:")
                            time.sleep(1)           
                            print()
                            print(resultset)
                            
                            print()
                            print("Return to menu?")
                            time.sleep(.5)
                            print()
                            time.sleep(.5)
                            coa = input("Enter 'y' for yes OR 'n' for exit: ").strip().casefold()
                            time.sleep(.5)
                            if coa[0] == 'y':
                                os.system("clear")
                                menu()
                                options = [1, 2, 3, 4]
                                operation = input("Enter function #: ")
                                time.sleep(.5)
                                if operation == "exit":
                                    end()                      
                                elif ((operation.isdigit() == False) or (int(operation) not in options)):
                                    end()
                                else:
                                    pass
                            
                            if coa[0] != 'y':  
                                end()
                        
                        elif attribute not in columns:
                            os.system("clear") 
                            print()
                            print ("Table field enter does not exist.")  
                            time.sleep(1)
                            end()
                            
            elif int(operation) == 3:
                os.system("clear")
                print()
                print("Selection: 3. Insert record")
                time.sleep(.5)
                print()
                print("Select table:")
                query ="""
                select  --*,
                        table_name
                from    information_schema.tables
                where   table_catalog = 'library'
                        and table_schema = 'public'
                        and table_name not like '%book_authors%';
                """
                print()
                print("Querying database tables...")
                cur.execute(query)
                resultset = cur.fetchall()
                
                tables = []                    
                for row in resultset:
                    rowx = ''.join(row)
                    rowx = rowx.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                    tables.append(rowx)
                
                print()
                print("Printing tables:")
                time.sleep(1)
                print()
                for table in tables:
                    print(table)
                    time.sleep(.25)
                    
                print() 
                ioperation = input("Enter table: ")
                time.sleep(.5)
                if ioperation == "exit":
                    end()
                                                              
                elif ioperation.isdigit() == False and ioperation.lower() in tables:
                    
                    intFields = []
                    query = f"""
                                select distinct 	column_name --, data_type 
                                from 				information_schema."columns"
                                where 				table_catalog = 'library'
                                                    and data_type in ('bigint', 'numeric', 'smallint', 'int', 'integer')
                                                    and table_name = '{ioperation}';   
                            """
                    cur.execute(query)
                    resultset = cur.fetchall()
                    for fields in resultset:
                        fieldx = ''.join(fields)
                        fieldx = fieldx.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                        intFields.append(fieldx) 
                    
                    dateFields = []
                    dateFields2 = ['dob', 'due', 'date', ]
                    query = f"""
                                select distinct 	column_name --, data_type 
                                from 				information_schema."columns"
                                where 				table_catalog = 'library'
                                                    and data_type like '%date%'
                                                    and table_name = '{ioperation}';   
                            """
                    cur.execute(query)
                    resultset = cur.fetchall()
                    for fields in resultset:
                        fieldx = ''.join(fields)
                        fieldx = fieldx.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                        dateFields.append(fieldx)
                        
                    tsFields = []
                    query = f"""
                                select distinct 	column_name --, data_type 
                                from 				information_schema."columns"
                                where 				table_catalog = 'library'
                                                    and data_type like'%timestamp%'
                                                    and table_name = '{ioperation}';   
                            """
                    cur.execute(query)
                    resultset = cur.fetchall()
                    for fields in resultset:
                        fieldx = ''.join(fields)
                        fieldx = fieldx.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                        tsFields.append(fieldx)

                    os.system("clear")
                    print()
                    print(f"Querying database for fields and datatypes in {ioperation} ...")
                    query = f"""
                            select 	column_name, data_type
                            from 	information_schema.columns
                            where 	table_name = '{ioperation}';
                            """
                    cur.execute(query)
                    resultset = cur.fetchall()
                    datatypes = {}
                    for column in resultset:
                        columnx = str(column)
                        columnx = columnx.strip().replace(')', '').replace('(', '').replace("'", "")
                        x = columnx.split(', ')
                        field = x[0]
                        datatype = x[1]
                        datatypes.update({field : datatype})
                    
                    query = f"""
                            select  count(*)
                            from 	information_schema.columns
                            where 	table_name = '{ioperation.lower()}';
                            """
                    cur.execute(query)
                    resultset2 = cur.fetchone()
                    columnCount = (str(resultset2))
                    columnCount = columnCount.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                    columnCount = int(columnCount)
                    counter = 0
                    
                    insertQuery =   f'''
                                        insert into {ioperation}
                                        columnClause
                                        values
                                        '''
                    columnClause = ''
                    
                    query = f"""
                                select distinct 	column_name --, data_type 
                                from 				information_schema."columns"
                                where 				table_catalog = 'library'
                                                    and table_name = '{ioperation}';   
                            """ 
                    cur.execute(query)
                    resultset = cur.fetchall()
                    for field in resultset:
                        fieldx = str(field)
                        fieldx = fieldx.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                        counter = counter + 1 
                        if ((fieldx not in tsFields) and (fieldx not in dateFields) and (fieldx.find('modified') < 0) and (fieldx.find('created') < 0)) or (fieldx in dateFields2):
                            print()
                            if fieldx in dateFields2:
                                print(f"{fieldx.capitalize()} field has datatype '{datatypes.get(fieldx)}'")
                                print()
                                fieldValue = input(f"Provide value formatted as 'YYYY-MM-DD' for field '{fieldx}' : ")
                                time.sleep(.5)
                            if fieldx == 'id':
                                query = f'select max({fieldx}) from {ioperation};'
                                cur.execute(query)
                                resultset = cur.fetchone()
                                newID = str(resultset)
                                newID = newID.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                                fieldValue = str(int(newID) + 1)
                                print(f"Record ID is {fieldValue} ")
                                confirmQuery = f'''select * from {ioperation} where {fieldx} = {fieldValue}'''
                                
                            if (fieldx not in dateFields2) and (fieldx != 'id'):
                                print(f"{fieldx.capitalize()} field has datatype '{datatypes.get(fieldx)}'")
                                print()
                                fieldValue = input(f"Provide value for field '{fieldx}' : ")
                                time.sleep(.5)
                                
                        if ((fieldx == 'modified_staff_id') or (fieldx == 'created_staff_id')):
                            fieldValue = '999'
                        if fieldx in tsFields:
                            current_date = datetime.now()
                            current_date = current_date.strftime('%Y-%m-%d %H:%M:%S')
                            fieldValue = current_date
                        if (fieldx in dateFields) and (fieldx not in dateFields2) :
                            current_date = datetime.now()
                            current_date = current_date.strftime('%Y-%m-%d')
                            fieldValue = current_date
                        if fieldx not in intFields:
                            fieldValue =  fieldValue.strip().replace("'", "''")
                            fieldValue = "'" + fieldValue + "'"
                        if fieldx in intFields:
                            fieldValue =  fieldValue.strip().replace("'", " ")
                        if ((counter == 1) and (fieldx in intFields)):
                            insertQuery = insertQuery + f'( {fieldValue} ,'
                            columnClause = columnClause + '(' + fieldx + ','
                        if ((counter == 1) and (fieldx not in intFields)):
                            insertQuery = insertQuery + f'( {fieldValue} ,'
                            columnClause = columnClause + '(' + fieldx + ','        
                        if ((counter > 1) and (counter < columnCount)):
                            insertQuery = insertQuery + ' ' + fieldValue + ','
                            columnClause = columnClause + ' ' + fieldx + ','
                        if counter == columnCount:
                            insertQuery = insertQuery + ' ' + fieldValue + ') ;'
                            columnClause = columnClause + ' ' + fieldx + ')'
                            print()
                            
                    insertQuery = insertQuery.replace('columnClause', f'{columnClause}')
                    cur.execute(insertQuery)
                    conn.commit()
                    os.system("clear")
                    print()
                    print("Creating record...")
                    time.sleep(1)
                    print()
                    print("Querying new record...")
                    time.sleep(1)
                    os.system("clear")
                    cur.execute(confirmQuery)
                    resultset = cur.fetchall()
                    for row in resultset:
                        formatted_row = list(row)
                        for i, item in enumerate(formatted_row):
                            if isinstance(item, datetime):
                                formatted_row[i] = item.strftime('%Y-%m-%d %H:%M:%S')
                        resultset = tuple(formatted_row)
                        
                    print()
                    print("Printing new record:")    
                    time.sleep(1)      
                    print()
                    print(resultset)
                    time.sleep(1)
                    
                    print()
                    print("Return to menu?")
                    time.sleep(.5)
                    print()
                    coa = input("Enter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.5)
                    if coa[0] == 'y':
                        menu()
                        options = [1, 2, 3, 4]
                        operation = input("Enter function #: ")
                        time.sleep(.25)
                        if operation == "exit":
                            end()                      
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end()
                        else:
                            pass
                    
                    if coa[0] != 'y':
                        end()  
                            
            elif int(operation) == 4:
                os.system("clear")
                print()
                print("Selection: 4. Delete record")
                time.sleep(.5)
                print()
                print("Querying database...")
                time.sleep(1)
                os.system("clear")
                query ="""
                select  --*,
                        table_name
                from    information_schema.tables
                where   table_catalog = 'library'
                        and table_schema = 'public'
                        and table_name not like '%book_authors%';
                """
                cur.execute(query)
                resultset = cur.fetchall()
                tables = []                    
                for row in resultset:
                    rowx = ''.join(row)
                    rowx = rowx.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                    tables.append(rowx)
                
                print()
                print("Printing tables:")
                time.sleep(1)
                print()
                for table in tables:
                    print(table)
                    time.sleep(.25)
                    
                print() 
                doperation = input("Enter table: ")
                time.sleep(.5)
                if doperation == "exit":
                    end()
                                                              
                elif doperation.isdigit() == False and doperation.lower() in tables:
                    os.system("clear")
                    print()
                    print("Querying database for table definition...")
                    query = f"""
                    select  string_agg(column_name, ' , ') as column_string
                    from 	information_schema.columns
                    where 	table_name = '{doperation.lower()}';
                    """
                    cur.execute(query)
                    resultset = cur.fetchall()
                    resultset_mod = str(resultset[0])
                    pos = resultset_mod.rfind(",")
                    replacement = ''
                    resultset_mod = resultset_mod[:pos] + replacement + resultset_mod[pos+1:]
                    resultset_mod = resultset_mod.replace(" , ", "' , '")
                                               
                    query = f"select * from {doperation.lower()};"
                    cur.execute(query)
                    resultset2 = cur.fetchall()
                    print()
                    print(f"Printing '{doperation}' table records:")
                    time.sleep(1)
                    print()
                    print(resultset_mod)
                    print()
                    ouput_dt_convert(resultset2)
                    print()
                    print(resultset_mod) 
                        
                    print()
                    print("Unique identifier (id) of record to be deleted required.")
                    time.sleep(.5)
                    print()
                    print("Enter 'exit' to exit utility")
                    time.sleep(.5)
                    print()
                    pkey = input("Enter id: ")
                    time.sleep(.5)
                    if pkey == "exit":
                        end()
                                                              
                    elif pkey.isdigit() == True and int(pkey) > 0:
                        os.system("clear")
                        pkey = int(pkey)
                        print()
                        query =f"""
                                delete from {doperation.lower()}
                                where id = {pkey};"""
                        cur.execute(query)
                        conn.commit()
                        print("Deleting record...")
                        time.sleep(1) 
                        print()
                        # print(f"Database message: {resultset}")
                        print("Querying table records...")
                        time.sleep(1)
                        os.system("clear")
                        query = f"""select * from {doperation} 
                                    where   (id < ({pkey} + 5))
                                            and (id > ({pkey} - 5));"""
                        cur.execute(query)
                        resultset = cur.fetchall()
                        print()
                        print("Printing records (with id +/- 5 than deleted record id):")        
                        time.sleep(1)   
                        print()
                        ouput_dt_convert(resultset)
                        print()
                        print("Return to menu?")
                        time.sleep(.5)
                        print()
                        coa = input("Enter 'y' for yes OR 'n' for exit: ").strip().casefold()
                        time.sleep(.5)
                        if coa[0] == 'y':
                            menu()
                            options = [1, 2, 3, 4]
                            operation = input("Enter function #: ")
                            time.sleep(.5)
                            if operation == "exit":
                                end()                     
                            elif ((operation.isdigit() == False) or (int(operation) not in options)):
                                end()
                            else:
                                pass
                        
                        if coa[0] != 'y':     
                            end()                






