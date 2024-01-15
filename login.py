import sys 

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