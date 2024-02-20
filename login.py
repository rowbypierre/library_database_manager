import sys 

def logon():
    xusername = 'user'
    xpassword = 'password'
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
        elif (uthreshold == 10) and (username != xusername):
            print("")
            print("Terminating script...")
            sys.exit()
        elif username == xusername:
            print("")
            print(f"Welcome {username}")
        
            while status == "locked":
                
                print("")
                password = input("Enter password: ").lower().strip()
                pthreshold += 1
            
                if (pthreshold == 9):
                    print("")
                    print("Last attempt before script terminates.")
                elif pthreshold == 10 and (password != xpassword):
                    print("")
                    print("Terminating script...")
                    sys.exit()
                elif password == xpassword:
                    print("")
                    print(f"Correct password entered for username: {username}")
                    status = "unlocked"