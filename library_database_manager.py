import psycopg2
import sys
from config import config
from login import logon
import datetime

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
                print("Option 1     (Execute stored queries)")
                print("or Option 2  (Update record)")
                print("or Option 3  (Create Record)")
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
                print("Queries include: ")
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
                    operation = "character"  
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
                    operation = "character"  
                    cur.close()
                    sys.exit() 
                                                              
                elif uoperation.isdigit() == False and uoperation.lower() in tables:
                    print("")
                    print("Querying database...")
                    query = f"""
                    select  string_agg(column_name, ' ,') as column_string
                    from 	information_schema.columns
                    where 	table_name = '{uoperation.lower()}';
                    """
                    cur.execute(query)
                    resultset = cur.fetchall()
                        
                    query = f"select * from {uoperation.lower()};"
                    cur.execute(query)
                    resultset2 = cur.fetchall()
                    resultset = resultset + resultset2
                    print("")
                    print("Printing table records...")
                    for row in resultset:
                        print(row)
                        
                    print("")
                    print("Select primary key of record to be updated.")
                    print("")
                    pkey = input("Enter primary key: ")
                    if pkey == "exit":
                        print("")
                        print("Exiting...")
                        operation = "character"  
                        cur.close()
                        sys.exit() 
                                                              
                    elif pkey.isdigit() == True and int(pkey) > 0:
                        
                        pkey = int(pkey)
                        print("")
                        print(f"Querying database, retrieving {uoperation} layout")
                        print("Printing field : datatype")
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
                            datatypes.update({field : datatype})
                            columns.append(field)
                            
                        print("")
                        attribute = input("Select field to update: ")
                        attribute = attribute.strip().lower()
                        
                        if attribute in columns:
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
                                print("")
                            
                            if ((attribute not in tsFields) and (attribute not in dateFields)): 
                                newValue = input("Enter new value for field: ")
                                if attribute not in intFields:
                                    newValue =  newValue.strip().replace("'", "''")
                                    newValue = "'" + newValue + "'"
                                elif attribute in intFields: 
                                    newValue = int(newValue)
                            elif attribute in tsFields:     
                                newValue = input(f"Provide value formatted as 'YYYY-MM-DD' for {attribute}: ")
                            elif attribute in dateFields:
                                newValue = input(f"Provide value formatted as 'YYYY-MM-DD hh:mm:ss' for {attribute}: ")
                                    
                            query =f"""
                                    update {uoperation}
                                    set {field} = {newValue}
                                    where id = {pkey};
                                    
                                    commit; """
                            cur.execute(query)
                            print("")
                            print("Updating record...")
                            print("")
                            # print(f"Database message: {resultset}")
                            print("Querying updated record...")
                            query = f"""select * from {uoperation} where id = {pkey};"""
                            cur.execute(query)
                            resultset = cur.fetchone()
                            print("")
                            print("Printing updated record...")           
                            print("")
                            print(resultset)
                            print("")
                            print("Exiting...")
                            print("")
                            print("Closing connection...")
                            operation = "character"  
                            cur.close()
                            sys.exit()
                        
                        else: 
                            print("")
                            print ("Table field enter does not exist")                           
                            print("")
                            print("Exiting...")
                            print("")
                            print("Closing connection...")
                            operation = "character"  
                            cur.close()
                            sys.exit()
                            
            elif int(operation) == 3:
                print("")
                print("You've selected 3. Insert record(s)")
                print("")
                print("Select table:")
                query ="""
                select  --*,
                        table_name
                from    information_schema.tables
                where   table_catalog = 'library'
                        and table_schema = 'public';
                """
                print("")
                print("Quering database tables...")
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
                ioperation = input("Enter table: ")
                if ioperation == "exit":
                    print("")
                    print("Exiting...")
                    print("")
                    print("Closing connection...")
                    operation = "character"  
                    cur.close()
                    sys.exit() 
                                                              
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
                            
                    # print("")
                    # print(f"Querying database for fields in {ioperation} ...")
                    # query = f"""
                    #         select  string_agg(column_name, ' ,') as column_string
                    #         from 	information_schema.columns
                    #         where 	table_name = '{ioperation.lower()}';
                    #         """
                    # cur.execute(query)
                    # resultset4 = cur.fetchone()
                    # print("")
                    # print(resultset4)
                    
                    print("")
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
                    columnCount = ''.join(str(resultset2))
                    columnCount = columnCount.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                    columnCount = int(columnCount)
                    
                    
                    print("")
                    print("Printing table columns...")
                    counter = 0
                    query = f"""
                                select distinct 	column_name --, data_type 
                                from 				information_schema."columns"
                                where 				table_catalog = 'library'
                                                    and table_name = '{ioperation}';   
                            """ 
                    cur.execute(query)
                    resultset = cur.fetchall()
                    insertQuery =   f'''
                                        insert into {ioperation}
                                        columnClause
                                        values
                                        '''
                    columnClause = ''
                    
                    for field in resultset:
                        fieldx = ''.join(field)
                        fieldx = fieldx.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                        counter = counter + 1 
                        if ((fieldx not in tsFields) and (fieldx not in dateFields) and (fieldx.find('modified') < 0) and (fieldx.find('created') < 0)) or (fieldx in dateFields2):
                            print("")
                            if fieldx in dateFields2:
                                print(f"{fieldx.capitalize()} field has datatype '{datatypes.get(fieldx)}'")
                                fieldValue = input(f"Provide value formatted as 'YYYY-MM-DD' for {fieldx}: ")
                            if fieldx == 'id':
                                query = f'select max({fieldx}) from {ioperation};'
                                cur.execute(query)
                                resultset = cur.fetchone()
                                newID = str(resultset)
                                newID = newID.replace("'","").replace(",","").replace(")","").replace("(","").strip()
                                fieldValue = str(int(newID) + 1)
                                print(f"Record ID is {fieldValue} ")
                                
                                confirmQuery = f''' select * from {ioperation} where {fieldx} = {fieldValue}'''
                            if (fieldx not in dateFields2) and (fieldx != 'id'):
                                print(f"{fieldx.capitalize()} field has datatype '{datatypes.get(fieldx)}'")
                                fieldValue = input(f"Provide value for {fieldx}: ")
                                
                        if ((fieldx == 'modified_staff_id') or (fieldx == 'created_staff_id')):
                            fieldValue = '999'
                        if fieldx in tsFields:
                            current_date = datetime.datetime.now()
                            current_date = current_date.strftime('%Y-%m-%d %H:%M:%S')
                            fieldValue = current_date
                        if (fieldx in dateFields) and (fieldx not in dateFields2) :
                            current_date = datetime.datetime.now()
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
                            print("")
                            print("Printing insert statement...")
                            print("")
                            
                    insertQuery = insertQuery.replace('columnClause', f'{columnClause}')
                    
                    cur.execute(insertQuery)
                    cur.commit()
                    print("")
                    print("Creating record...")
                    print("")
                    print("Querying new record...")
                    cur.execute(confirmQuery)
                    resultset = cur.fetchone()
                    print("")
                    print("Printing updated record...")           
                    print("")
                    print(resultset)
                    print("")
                    print("Exiting...")
                    print("")
                    print("Closing connection...")
                    operation = "character"  
                    cur.close()
                    sys.exit()     
                            
            elif int(operation) == 4:
                print("")
                print("You've selected 4. Delete record")
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
                doperation = input("Enter table: ")
                if doperation == "exit":
                    print("")
                    print("Exiting...")
                    print("")
                    print("Closing connection...")
                    operation = "character"  
                    cur.close()
                    sys.exit() 
                                                              
                elif doperation.isdigit() == False and doperation.lower() in tables:
                    print("")
                    print("Querying database...")
                    query = f"""
                    select  string_agg(column_name, ' ,') as column_string
                    from 	information_schema.columns
                    where 	table_name = '{doperation.lower()}';
                    """
                    cur.execute(query)
                    resultset = cur.fetchall()
                        
                    query = f"select * from {doperation.lower()};"
                    cur.execute(query)
                    resultset2 = cur.fetchall()
                    resultset = resultset2 + resultset 
                    print("")
                    print("Printing table records...")
                    for row in resultset:
                        print(row)
                        
                    print("")
                    print("Select id to be deleted.")
                    print("")
                    pkey = input("Enter id: ")
                    if pkey == "exit":
                        print("")
                        print("Exiting...")
                        operation = "character"  
                        cur.close()
                        sys.exit() 
                                                              
                    elif pkey.isdigit() == True and int(pkey) > 0:
                        pkey = int(pkey)
                        print("")
                        query =f"""
                                delete from {doperation.lower()}
                                where id = {pkey};"""
                        cur.execute(query)
                        print("Deleting record...")
                        print("")
                        # print(f"Database message: {resultset}")
                        print("Querying table records...")
                        query = f"""select * from {doperation} 
                                where   (id < ({pkey} + 5))
                                        or (id > ({pkey} - 5));"""
                        cur.execute(query)
                        resultset = cur.fetchall()
                        print("")
                        print("Printing records (with id greater (+ 5) or less (- 5) than deleted record)...")           
                        print("")
                        for row in resultset:
                            print(row)
                        print("")
                        print("Exiting...")
                        print("")
                        print("Closing connection...")
                        operation = "character"  
                        cur.close()
                        sys.exit()                  






