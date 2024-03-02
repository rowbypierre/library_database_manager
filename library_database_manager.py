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
    
Enter 'exit' to exit utility"""
def clear():
    os.system("cls" if os.name == "nt" else "clear")
    
def menu():
    clear()
    print(f"\n{menuMessage}")
    time.sleep(1.5)

def ouput_dt_convert(resultset):
    for row in resultset:
        formatted_row = list(row)
        for i, item in enumerate(formatted_row):
            if isinstance(item, datetime):
                formatted_row[i] = item.strftime('%Y-%m-%d %H:%M:%S')
        print(tuple(formatted_row))
        time.sleep(.25)

if __name__ == '__main__':
    clear()
    logon()
    
    print('\nConnecting to server: "localhost" database: "library"')
    time.sleep(1.5)
    parms = config()
    conn = psycopg2.connect(**parms)
    cur = conn.cursor()
    
    def end():
        clear()
        
        print("\nClosing connection...")
        time.sleep(1.5)
        
        print("\nExiting program...")
        time.sleep(1.5)
        cur.close()
        clear()
        sys.exit()
    
    print("\nConnection established...")
    time.sleep(1.5)
    clear()
    
    print("\nQuerying database version...")
    time.sleep(1.5)
    cur.execute('select version();')
    db_version = cur.fetchone()
    db_version = str(db_version).replace("'","").replace(",","").replace(")","").replace("(","").strip()
    print(f"\n PostgreSQL version: {db_version}")
    time.sleep(1.5)
    
    menu()
    
    operation = input("\nEnter function #: ")
    time.sleep(.75)
    if operation == "exit":
        end()   
    elif operation.isdigit() == False: 
        print("\nNumeric value not entered") 
        time.sleep(1.5)
        end()
    else:
        
        while operation.isdigit() == True:    
            if int(operation) > 4 or int(operation) < 1:
                menu()
                operation = input("\nEnter function #: ")
                time.sleep(.75)
                if operation == "exit":
                    end()                      
                elif operation.isdigit() == False:
                    end()
            elif int(operation) == 1:
                clear()
                print("\nSelection: 1. Execute query")
                time.sleep(.75)       
                print("\nQueries include: ")
                print("1. Library catalog")
                print("2. Catalog physical condition")
                print("3. Available books")
                print("4. Shelf warmers")
                print("5. Book checkout durations")
                print("6. Overdue returns")
                print("7. Book fines summary")
                print("8. Monthly loans # (time series)")
                print("9. Patron Activity")
                
                qoperation = input("\nEnter # (1-9) for query: ")
                time.sleep(.75)
                if qoperation == "exit":
                    end()                                            
                elif qoperation.isdigit() == True and int(qoperation) == 1: 
                    clear()                   
                    print("\nQuerying database...")
                    time.sleep(1.5)
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
                    print("\nPrinting resultset...")
                    time.sleep(1.5)
                    os.system('clear')
                    print(f"\n{header} \n")
                    for row in resultset:
                        print(row)
                        time.sleep(.25) 
                    print(f"\n{header} \n")
                    
                    print("\nReturn to menu?")
                    time.sleep(.75)
                    coa = input("\nEnter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.75)
                    if coa[0] == 'y':
                        menu()
                        options = [1, 2, 3, 4]
                        operation = input("\nEnter function #: ")
                        time.sleep(.75)
                        if operation == "exit":
                            end()                     
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end()
                        else:
                            pass
                    if coa[0] != 'y':   
                        end()
                
                elif qoperation.isdigit() == True and int(qoperation) == 2:
                    clear()                    
                    print("\nQuerying database...")
                    time.sleep(1.5)
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
                    print("\nPrinting resultset...")
                    time.sleep(1.5)
                    os.system('clear')
                    print(f"\n{header} \n")
                    for row in resultset:
                        print(row)
                        time.sleep(.25)
                    print(f"\n{header} \n")  
                      
                    print("\nReturn to menu?")
                    time.sleep(.75)
                    coa = input("\nEnter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.75)
                    if coa[0] == 'y':
                        menu()
                        options = [1, 2, 3, 4]
                        operation = input("\nEnter function #: ")
                        time.sleep(.75)
                        if operation == "exit":
                            end()                     
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end()
                        else:
                            pass
                    if coa[0] != 'y': 
                        end()
                    
                elif qoperation.isdigit() == True and int(qoperation) == 3:   
                    clear()                 
                    print("\nQuerying database...")
                    time.sleep(1.5)
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
                    print("\nPrinting resultset...")
                    time.sleep(1.5)
                    os.system('clear')
                    print(f"\n{header} \n")   
                          
                    for row in resultset:
                        print(row)
                        time.sleep(.75)
                    
                    print(f"\n{header} \n")   
                    
                    
                    print("\nReturn to menu?")
                    time.sleep(.75)
                    
                    coa = input("\nEnter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.75)
                    if coa[0] == 'y':
                        menu()
                        options = [1, 2, 3, 4]
                        operation = input("\nEnter function #: ")
                        time.sleep(.75)
                        if operation == "exit":
                            end()                    
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end()
                        else:
                            pass
                        
                    if coa[0] != 'y':   
                        end()
                    
                elif qoperation.isdigit() == True and int(qoperation) == 4:
                    clear()                    
                    print("\nQuerying database...")
                    time.sleep(1.5)
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
                    
                    cur.execute(query)
                    resultset = cur.fetchall()
                    header = '(Book Title, Author First Name, Author Last Name, Author MI)' 
                    print("\nPrinting resultset...")
                    time.sleep(1.5)
                    os.system('clear')
                    print(f"\n{header} \n")    
                    for row in resultset:
                        print(row)
                        time.sleep(.25)
                    print(f"\n{header} \n")
                    
                    print("\nReturn to menu?")
                    time.sleep(.75)
                    coa = input("\nEnter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.75)
                    if coa[0] == 'y':
                        clear()
                        menu()
                        options = [1, 2, 3, 4]
                        operation = input("\nEnter function #: ")
                        time.sleep(.75)
                        if operation == "exit":
                            end()                     
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end()
                        else:
                            pass
                    if coa[0] != 'y': 
                        end()
                    
                elif qoperation.isdigit() == True and int(qoperation) == 5:     
                    clear()  
                    print("\nQuerying database...")
                    time.sleep(1.5)
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
                    cur.execute(query)
                    resultset = cur.fetchall()
                    print("\nPrinting resultset...")
                    time.sleep(1.5)
                    os.system('clear')
                    header = '(Book Title, Days Loaned)'
                    print(f"\n{header} \n")
                    for row in resultset:
                        print(row)
                        time.sleep(.25)
                    print(f"\n{header} \n")
                    
                    print("\nReturn to menu?")
                    time.sleep(.75)
                    coa = input("\nEnter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.75)
                    if coa[0] == 'y':
                        clear()
                        menu()
                        options = [1, 2, 3, 4]
                        operation = input("\nEnter function #: ")
                        time.sleep(.75)
                        if operation == "exit":
                            end()                     
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end()
                        else:
                            pass
                        
                    if coa[0] != 'y': 
                        end()
                    
                elif qoperation.isdigit() == True and int(qoperation) == 6:     
                    clear()              
                    print("\nQuerying database...")
                    time.sleep(1.5)
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
                    print("\nPrinting resultset...")
                    time.sleep(1.5)
                    os.system('clear')
                    print(f"\n{header} \n")                    
                    
                    for row in resultset:
                        print(row)
                        time.sleep(.25)
                    print(f"\n{header} \n")
                    
                    print("\nReturn to menu?")
                    time.sleep(.75)
                    coa = input("\nEnter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.75)
                    if coa[0] == 'y':
                        clear()
                        menu()
                        options = [1, 2, 3, 4]
                        operation = input("\nEnter function #: ")
                        time.sleep(.75)
                        if operation == "exit":
                            end()                     
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end()
                        else:
                            pass
                    if coa[0] != 'y':  
                        end()
                    
                elif qoperation.isdigit() == True and int(qoperation) == 7:   
                    clear()               
                    print("\nQuerying database...")
                    time.sleep(1.5)
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
                    print("\nPrinting resultset...")
                    time.sleep(1.5)
                    os.system('clear')
                    print(f"\n{header} \n")
                    for row in resultset:
                        print(row)
                        time.sleep(.25)
                    print(f"\n{header} \n")
                    
                    
                    print("\nReturn to menu?")
                    time.sleep(.75)
                    coa = input("\nEnter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.75)
                    if coa[0] == 'y':
                        clear()
                        menu()                       
                        options = [1, 2, 3, 4]
                        operation = input("\nEnter function #: ")
                        time.sleep(.75)
                        if operation == "exit":
                            end()                     
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end() 
                        else:
                            pass
                    
                    if coa[0] != 'y':
                        end()              
                
                elif qoperation.isdigit() == True and int(qoperation) == 8:   
                    clear()               
                    print("\nQuerying database...")
                    time.sleep(1.5)
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
                    print("\nPrinting resultset...")
                    time.sleep(1.5)
                    os.system('clear')
                    print(f"\n{header} \n")
                    for row in resultset:
                        print(row)
                        time.sleep(.25)
                    print(f"\n{header} \n")
                    
                    print("\nReturn to menu?")
                    time.sleep(.75)
                    coa = input("\nEnter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.75)
                    if coa[0] == 'y':
                        clear()
                        menu()                       
                        options = [1, 2, 3, 4]
                        operation = input("\nEnter function #: ")
                        time.sleep(.75)
                        if operation == "exit":
                            end()                     
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end() 
                        else:
                            pass
                    
                    if coa[0] != 'y':
                        end()  
                
                elif qoperation.isdigit() == True and int(qoperation) == 9:   
                    clear()               
                    print("\nQuerying database...")
                    time.sleep(1.5)
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
                    print("\nPrinting resultset...")
                    time.sleep(1.5)
                    os.system('clear')
                    print(f"\n{header} \n")
                    for row in resultset:
                        print(row)
                        time.sleep(.25)
                    print(f"\n{header} \n")
                    
                    print("\nReturn to menu?")
                    time.sleep(.75)
                    coa = input("\nEnter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.75)
                    if coa[0] == 'y':
                        clear()
                        menu()                       
                        options = [1, 2, 3, 4]
                        operation = input("\nEnter function #: ")
                        time.sleep(.75)
                        if operation == "exit":
                            end()                     
                        elif ((operation.isdigit() == False) or (int(operation) not in options)):
                            end() 
                        else:
                            pass
                    
                    if coa[0] != 'y':
                        end() 
                        
                else:                    
                    print("\nEnter numeric value between 1 - 9")
                    time.sleep(.75)
                                            
            elif int(operation) == 2:
                clear()
                print("\nSelection: 2. Update record")
                time.sleep(.75)
                print("\nQuerying database tables...")
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
                print("\nPrinting tables: \n")
                time.sleep(1.5)
                for table in tables:
                    print(table)
                    time.sleep(.25)
                    
                uoperation = input("\nEnter table: ")
                time.sleep(.75)
                if uoperation == "exit":
                    end()
                elif uoperation.isdigit() == False and uoperation.lower() in tables:
                    clear()
                    print("\nQuerying database...")
                    time.sleep(1.5)
                    clear()
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
                    print(f"\nPrinting '{uoperation}' table records:")
                    time.sleep(1.5)
                    print(f"\n{targetTemplate} \n")
                    ouput_dt_convert(resultset2)
                    time.sleep(.25)
                    print(f"\n{targetTemplate} \n")
                    print("\nUnique identifier (id) from above required.")
                    time.sleep(.75)
                    
                    pkey = input("\nEnter id: ")
                    time.sleep(.75)
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
                        clear()
                        print(f"\nQuerying database, retrieving {uoperation} table definiton...")
                        time.sleep(1.5)
                        print("\nFields:")
                        time.sleep(.75)
                        print("\n'data field' : 'datatype'")
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
                        print("\n\nRecord: ")
                        time.sleep(.75)
                        print(f"\n{targetTemplate}")
                        print(targetRecord)
                        time.sleep(.25)    
                        
                        attribute = input("\nEnter field to update: ")
                        time.sleep(.75)
                        attribute = attribute.strip().lower()
                        if attribute in columns:
                            clear()
                            print(f"\n{attribute.capitalize()} field has datatype: '{datatypes.get(attribute)}'")
                            
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
                            
                            
                            print(f"\n{targetTemplate}")
                            print(targetRecord)    
                            
                            if ((attribute not in tsFields) and (attribute not in dateFields)): 
                                newValue = input(f"\nEnter new value for {attribute}: ")
                                time.sleep(.75)
                                if attribute not in intFields:
                                    newValue =  newValue.strip().replace("'", "''")
                                    newValue = "'" + newValue + "'"
                                elif attribute in intFields: 
                                    newValue = int(newValue)
                           
                            elif attribute in dateFields:
                                newValue = input(f"\nProvide value formatted as 'YYYY-MM-DD' for field '{attribute}' : ")
                                time.sleep(.75)
                            
                            elif attribute in tsFields:
                                newValue = input(f"\nProvide value formatted as 'YYYY-MM-DD hh:mm:ss' for field '{attribute}' : ")
                                time.sleep(.75)
                                    
                            query =f"""
                                    update {uoperation}
                                    set {attribute} = {newValue}
                                    where id = {pkey};
                                    
                                    commit; """
                            cur.execute(query)
                            clear()
                            print("\nUpdating record...")
                            time.sleep(1.5) 
                            print("\nQuerying updated record...")
                            time.sleep(1.5)
                            clear()
                            query = f"""select * from {uoperation} where id = {pkey};"""
                            cur.execute(query)
                            resultset = cur.fetchall()
                            for row in resultset:
                                formatted_row = list(row)
                                for i, item in enumerate(formatted_row):
                                    if isinstance(item, datetime):
                                        formatted_row[i] = item.strftime('%Y-%m-%d %H:%M:%S')
                                resultset = tuple(formatted_row)
                            print("\nPrinting updated record:")
                            time.sleep(1.5)           
                            print(f"\n{resultset}")
                            
                            print("\nReturn to menu?")
                            time.sleep(.75)
                            time.sleep(.75)
                            coa = input("\nEnter 'y' for yes OR 'n' for exit: ").strip().casefold()
                            time.sleep(.75)
                            if coa[0] == 'y':
                                clear()
                                menu()
                                options = [1, 2, 3, 4]
                                operation = input("\nEnter function #: ")
                                time.sleep(.75)
                                if operation == "exit":
                                    end()                      
                                elif ((operation.isdigit() == False) or (int(operation) not in options)):
                                    end()
                                else:
                                    pass
                            
                            if coa[0] != 'y':  
                                end()
                        
                        elif attribute not in columns:
                            clear() 
                            print("\nTable field enter does not exist.")  
                            time.sleep(1.5)
                            end()
                            
            elif int(operation) == 3:
                clear()
                print("\nSelection: 3. Insert record")
                time.sleep(.75)
                print("\nSelect table:")
                query ="""
                select  --*,
                        table_name
                from    information_schema.tables
                where   table_catalog = 'library'
                        and table_schema = 'public'
                        and table_name not like '%book_authors%';
                """
                print("\nQuerying database tables...")
                cur.execute(query)
                resultset = cur.fetchall()
                
                tables = [] 
                for row in resultset:
                    rowx = ''.join(row)
                    rowx = rowx.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                    tables.append(rowx)
                print("\nPrinting tables: \n")
                time.sleep(1.5)
                for table in tables:
                    print(table)
                    time.sleep(.25)
                 
                ioperation = input("\nEnter table: ")
                time.sleep(.75)
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

                    clear()
                    print(f"\nQuerying database for fields and datatypes in {ioperation} ...")
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
                            if fieldx in dateFields2:
                                print(f"\n{fieldx.capitalize()} field has datatype '{datatypes.get(fieldx)}'")
                                fieldValue = input(f"\nProvide value formatted as 'YYYY-MM-DD' for field '{fieldx}' : ")
                                time.sleep(.75)
                            if fieldx == 'id':
                                query = f'select max({fieldx}) from {ioperation};'
                                cur.execute(query)
                                resultset = cur.fetchone()
                                newID = str(resultset)
                                newID = newID.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                                fieldValue = str(int(newID) + 1)
                                print(f"\nRecord ID is {fieldValue} ")
                                confirmQuery = f'''select * from {ioperation} where {fieldx} = {fieldValue}'''
                            if (fieldx not in dateFields2) and (fieldx != 'id'):
                                print(f"\n{fieldx.capitalize()} field has datatype '{datatypes.get(fieldx)}'")
                                fieldValue = input(f"\nProvide value for field '{fieldx}' : ")
                                time.sleep(.75)
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
                            
                            
                    insertQuery = insertQuery.replace('columnClause', f'{columnClause}')
                    cur.execute(insertQuery)
                    conn.commit()
                    clear()
                    print("\nCreating record...")
                    time.sleep(1.5)
                    print("\nQuerying new record...")
                    time.sleep(1.5)
                    clear()
                    cur.execute(confirmQuery)
                    resultset = cur.fetchall()
                    for row in resultset:
                        formatted_row = list(row)
                        for i, item in enumerate(formatted_row):
                            if isinstance(item, datetime):
                                formatted_row[i] = item.strftime('%Y-%m-%d %H:%M:%S')
                        resultset = tuple(formatted_row)
                    print("\nPrinting new record:")    
                    time.sleep(1.5)      
                    print(f"\n{resultset}")
                    time.sleep(1.5)
                    
                    print("\nReturn to menu?")
                    time.sleep(.75)
                    coa = input("\nEnter 'y' for yes OR 'n' for exit: ").strip().casefold()
                    time.sleep(.75)
                    if coa[0] == 'y':
                        menu()
                        options = [1, 2, 3, 4]
                        operation = input("\nEnter function #: ")
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
                clear()
                print("\nSelection: 4. Delete record")
                time.sleep(.75)
                print("\nQuerying database...")
                time.sleep(1.5)
                clear()
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
                
                print("\nPrinting tables: \n")
                time.sleep(1.5)
                for table in tables:
                    print(table)
                    time.sleep(.25)
                    
                doperation = input("\nEnter table: ")
                time.sleep(.75)
                if doperation == "exit":
                    end()
                elif doperation.isdigit() == False and doperation.lower() in tables:
                    clear()
                    print("\nQuerying database for table definition...")
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
                    print(f"\nPrinting '{doperation}' table records:")
                    time.sleep(1.5)
                    print(f"\n{resultset_mod}")
                    ouput_dt_convert(resultset2)
                    print(f"\n{resultset_mod}") 
                        
                    
                    print("\nUnique identifier (id) of record to be deleted required.")
                    time.sleep(.75)
                    print("\nEnter 'exit' to exit utility")
                    time.sleep(.75)
                    pkey = input("\nEnter id: ")
                    time.sleep(.75)
                    if pkey == "exit":
                        end()
                    elif pkey.isdigit() == True and int(pkey) > 0:
                        clear()
                        pkey = int(pkey)
                        query =f"""
                                delete from {doperation.lower()}
                                where id = {pkey};"""
                        cur.execute(query)
                        conn.commit()
                        print("\nDeleting record...")
                        time.sleep(1.5) 
                        
                        # print(f"Database message: {resultset}")
                        print("\nQuerying table records...")
                        time.sleep(1.5)
                        clear()
                        query = f"""select * from {doperation} 
                                    where   (id < ({pkey} + 5))
                                            and (id > ({pkey} - 5));"""
                        cur.execute(query)
                        resultset = cur.fetchall()
                        print("\nPrinting records (with id +/- 5 than deleted record id): \n")        
                        time.sleep(1.5)   
                        ouput_dt_convert(resultset)
                        
                        print("\nReturn to menu?")
                        time.sleep(.75)
                        coa = input("\nEnter 'y' for yes OR 'n' for exit: ").strip().casefold()
                        time.sleep(.75)
                        if coa[0] == 'y':
                            menu()
                            options = [1, 2, 3, 4]
                            operation = input("\nEnter function #: ")
                            time.sleep(.75)
                            if operation == "exit":
                                end()                     
                            elif ((operation.isdigit() == False) or (int(operation) not in options)):
                                end()
                            else:
                                pass
                        
                        if coa[0] != 'y':     
                            end()                






