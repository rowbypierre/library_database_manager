import sys 

status = "locked" 
uthreshold = 0
pthreshold = 0

while status == "locked":
    
    username = input("Enter username: ").lower().strip()
    uthreshold += 1
    
    if uthreshold == 9:
        print("""
Last attempt before script terminates.""")
    elif (uthreshold == 10) and (username != "test"):
        print("""
Terminating script...""")
        sys.exit()
    elif username == "test":
        print(f"""
Welcome {username}""")
        
        while status == "locked":
            
            password = input("Enter password: ").lower().strip()
            pthreshold += 1
            
            if (pthreshold == 9):
                print("""
Last attempt before script terminates.""")
            elif pthreshold == 10 and (password != "password"):
                print("""
Terminating script...""")
                sys.exit()
            elif password == "password":
                prompt = f"""
Correct password entered for username: {username}"""
                print(prompt)
                status = "unlocked"

print(
"""
Library Database Management System Utility
    
Operations include:
    1. Query table
    2. Update records   
"""
)

operation = input("Enter operation: ")

if operation.isdigit() == False:
    print("""
Enter numeric value 1 or 2""")
elif int(operation) > 2 or int(operation) < 1:
    print("""
Select between Option 1 (Query Table) or Option 2 (Update record)""")
elif int(operation) == 1:
    print("""
You've 1. Query table""")
elif int(operation) == 2:
    print("""
2. Update records""")