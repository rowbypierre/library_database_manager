import sys, time 
from getpass import getpass

def logon():
    xusername = 'user'
    xpassword = 'password'
    status = "locked" 
    uthreshold = 0
    pthreshold = 0

    while status == "locked":
        
        print("")
        username = input("Enter username: ").lower().strip()
        time.sleep(1)
        uthreshold += 1
    
        if uthreshold == 9:
            print("")
            print("Last attempt before script terminates.")
            time.sleep(1)
        elif (uthreshold == 10) and (username != xusername):
            print("")
            print("Terminating script...")
            sys.exit()
        elif username == xusername:
            username = username.capitalize()
            print("")
            print(f"Welcome {username}")
            time.sleep(1)
        
            while status == "locked":
                
                print("")
                password = getpass("Enter password: ").lower().strip()
                time.sleep(1)
                pthreshold += 1
            
                if (pthreshold == 9):
                    print("")
                    print("Last attempt before script terminates.")
                    time.sleep(1)
                if pthreshold >= 1:
                    print("")
                    print("Incorrect password entrered for: " + username)
                elif pthreshold == 10 and (password != xpassword):
                    print("")
                    print("Terminating script...")
                    sys.exit()
                if password == xpassword:
                    print("")
                    print(f"Correct password entered for username: {username}")
                    time.sleep(1)
                    status = "unlocked"