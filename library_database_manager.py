import psycopg2
import sys
from config import config
from login import logon

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
    2. Update record
    3. Insert record
    4. Delete record
    
    Enter 'exit' to exit utility""")
    
    print("")
    operation = input("Enter operation: ")
    if operation == "exit":
        print("")
        print("Exiting...")
        cur.close()
        sys.exit()      
    
    elif operation.isdigit() == False:
        print("")
        print("Numeric value 1, 2, 3, or 4 not entered") 
        print("")
        print("Closing connection...")
        cur.close()
        print("")
        print("Exiting...")
    
    else:
        while operation.isdigit() == True:
            
            if int(operation) > 4 or int(operation) < 1:
                print("")
                print("Select between:")
                print("Option 1     (Query Table)")
                print("or Option 2  (Update record)")
                print("or Option 3  (Insert Record)")
                print("or Option 4  (Delete recod)")
                
                operation = input("Enter operation: ")
                if operation == "exit":
                    print("")
                    print("Exiting...")
                    operation = "character"  
                    cur.close()
                    sys.exit()                       
                elif operation.isdigit() == False:
                    print("")
                    print("Enter numeric value 1, 2, 3, or 4") 
                    print("")
                    print("Closing connection...")
                    cur.close()
                
            elif int(operation) == 1:
                print("")
                print("You've selected 1. Query table")
                print("")
                print("Tables to query include: ")
                print("1. Library catalog")
                print("2. Catalog physical condition")
                print("3. Available books")
                print("4. Shelf warmers")
                print("5. Book checkout durations")
                print("6. Overdue returns")
                print("7. Book fines summary")
                print("")
                
                qoperation = input("Enter selection: ")
                if qoperation == "exit":
                    print("")
                    print("Exiting...")
                    qoperation = "character"  
                    cur.close()
                    sys.exit() 
                                                              
                elif qoperation.isdigit() == True and int(qoperation) == 1:                    
                    query = ''' 
                            select 		title "Title", isbn "ISBN", genre "Genre", condition "Condition"
                            from        books b
                                        left join genres g on g.id = b.genre_id  
                                        left join conditions c on c.id = b.condition_id                   
                                        left join statuses s on s.id = b.status_id                   
                            order by	Genre, Title;'''
                    print("")
                    print("Quering database...")
                    cur.execute(query)
                    resultset = cur.fetchall()
                    
                    print("")
                    print("Printing database result...")
                    print("")
                    print('(Title, ISBN, Genre, Book Condition)')                    
                    for row in resultset:
                        print(row)
                                  
                    print("")
                    print("Closing connection...")
                    cur.close()                  
                    operation = "character"
                
                elif qoperation.isdigit() == True and int(qoperation) == 2:                    
                    query = ''' 
                            select      condition "Condition",			
                                        count(*) "Count",			
                                        concat((count(*) * 100/(select count(*) from books)) , '% of Books') "Percent"
                            from		books b
                                		left join conditions c on c.id = b.condition_id        
                            group by 	condition
                            order by    "Count" desc, condition;'''
                    print("")
                    print("Quering database...")
                    cur.execute(query)
                    resultset = cur.fetchall()
                    
                    print("")
                    print("Printing database result...")
                    print("")
                    print('(Condition, Count, Percent)')                    
                    for row in resultset:
                        print(row)
                
                    
                    print("")
                    print("Closing connection...")
                    cur.close()  
                    operation = "character"
                    
                elif qoperation.isdigit() == True and int(qoperation) == 3:                    
                    query = ''' 
                            select 		--*,
						                title as "Book Title",
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
                    print("")
                    print('(Book Title, Author First Name, Author Last Name, Author MI)')                    
                    for row in resultset:
                        print(row)
                
                    print("")
                    print("Closing connection...")
                    cur.close()                   
                    operation = "character"
                    
                elif qoperation.isdigit() == True and int(qoperation) == 4:                    
                    query = ''' 
                            select 		--*,
			                            title as "Book Title",
			                            fname as "Author First Name",
			                            lname as "Author Last Name",
			                            mi as "Author MI"
                            from 		book_authors  ba
			                            left join authors a on ba.author_id = a.id
			                            left join books b on ba.book_id = b.id 
			                            left join statuses s on b.status_id = s.id
                            where 		b.id not in (select book_id from loans)
                            order by 	title, fname, lname;'''
                    print("")
                    print("Quering database...")
                    cur.execute(query)
                    resultset = cur.fetchall()
                    
                    print("")
                    print("Printing database result...")
                    print("")
                    print('(Book Title, Author First Name, Author Last Name, Author MI)')                    
                    for row in resultset:
                        print(row)
                
                    print("")
                    print("Closing connection...")
                    cur.close()                   
                    operation = "character"
                    
                elif qoperation.isdigit() == True and int(qoperation) == 5:       
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
                    print("")
                    print("Quering database...")
                    cur.execute(query)
                    resultset = cur.fetchall()
                    
                    print("")
                    print("Printing database result...")
                    print("")
                    print('(Book Title, Days Loaned)')                    
                    for row in resultset:
                        print(row)
                
                    print("")
                    print("Closing connection...")
                    cur.close()                   
                    operation = "character"
                    
                elif qoperation.isdigit() == True and int(qoperation) == 6:                   
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
                    print("")
                    print("Quering database...")
                    cur.execute(query)
                    resultset = cur.fetchall()
                    
                    print("")
                    print("Printing database result...")
                    print("")
                    print('(Patron, Book, Checkout, Due, Returned, Days Overdue, Fine)')                    
                    for row in resultset:
                        print(row)
                
                    print("")
                    print("Closing connection...")
                    cur.close()                    
                    operation = "character"
                    
                elif qoperation.isdigit() == True and int(qoperation) == 7:                  
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
                    print("")
                    print("Quering database...")
                    cur.execute(query)
                    resultset = cur.fetchall()
                    
                    print("")
                    print("Printing database result...")
                    print("")
                    print('(Genre, Fine (AVG))')                    
                    for row in resultset:
                        print(row)
                
                    print("")
                    print("Closing connection...")
                    cur.close()                    
                    operation = "character"                
                
                else:                    
                    print("Enter numeric value between 1 - 7")
                                            
            elif int(operation) == 2:
                print("")
                print("You've selected 2. Update record")
                print("")
                print("Select source table:")
                query ="""
                select  --*,
                        table_name
                from    information_schema.tables
                where   table_catalog = 'library'
                        and table_schema = 'public';
                """
                print("")
                print("Quering database...")
                cur.execute(query)
                resultset = cur.fetchall()
                tables = []                    
                for row in resultset:
                    rowx = ''.join(row)
                    rowx = rowx.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                    tables.append(rowx)
                
                print("")
                print("Printing database tables...")
                print("")
                for table in tables:
                    print(table)
                
                print("") 
                uoperation = input("Enter table: ")
                if uoperation == "exit":
                    print("")
                    print("Exiting...")
                    print("")
                    print("Closing connection...")
                    qoperation = "character"  
                    cur.close()
                    sys.exit() 
                                                              
                elif uoperation.isdigit() == False and uoperation.lower() in tables:
                    print("")
                    print("Querying database...")
                    query = """
                    select  string_agg(column_name, ' ,') as column_string
                    from 	information_schema.columns
                    where 	table_name = '{}';
                    """.format(uoperation.lower())
                    cur.execute(query)
                    resultset1 = cur.fetchall()
                        
                    query = "select * from {}; ".format(uoperation.lower())
                    cur.execute(query)
                    resultset2 = cur.fetchall()
                    resultset = resultset1 + resultset2
                    print("")
                    print("Printing table records...")
                    for row in resultset:
                        print(row)
                        
                    print("")
                    print("Select primary key of record to be updated ")
                    print("")
                    pkey = input("Enter primary key: ")
                    if pkey == "exit":
                        print("")
                        print("Exiting...")
                        qoperation = "character"  
                        cur.close()
                        sys.exit() 
                                                              
                    elif pkey.isdigit() == True and int(pkey) > 0:
                        print("")
                        field = input("Select field to upate: ")
                        field = field.strip().lower()
                        print("")
                        newValue = input("Enter new value for field: ")
                        newValue =  newValue.strip()
                        
                        query ="""
                                update table {}
                                set {} = '{}'
                                where id = {};"""
                        query = query.format(uoperation,field, newValue, pkey)
                        
                        print("")
                        print("Updating record...")
                        print("")
                        print("Querying updated record...")
                        print("")
                        print("Printing updated record...")           
                        print("")
                        print(query)
                        print("")
                        print("Exiting...")
                        print("")
                        print("Closing connection...")
                        qoperation = "character"  
                        cur.close()
                        sys.exit()       
                    
                        
            elif int(operation) == 3:
                print("")
                print("You've selected 3. Insert record(s)")
            elif int(operation) == 4:
                print("")
                print("You've selected 4. Delete record(s)")






