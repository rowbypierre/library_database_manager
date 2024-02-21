import sys, os, time 
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
        time.sleep(.75)
        uthreshold += 1
    
        if username == xusername:
            username = username.capitalize()
            print("")
            print(f"Welcome {username}")
            time.sleep(.75)
            os.system("clear")
            
            while status == "locked":
                
                print("")
                password = getpass("Enter password: ").lower().strip()
                time.sleep(.75)
                pthreshold += 1
            
                if password == xpassword:
                    print("")
                    print(f"Correct password entered for username: {username}")
                    time.sleep(.75)
                    status = "unlocked"
                    os.system("clear")
                else:
                    if pthreshold == 9:
                        print("")
                        print("Last attempt before program terminates.")
                        time.sleep(.75)
                        os.system("clear")
                    if pthreshold in range (1, 8):
                        print("")
                        print("Incorrect password entered for: " + username)
                        time.sleep(.75)
                        os.system("clear")
                    elif pthreshold == 10:
                        print("")
                        print("Terminating program...")
                        os.system("clear")
                        sys.exit()
                        
        else:
            print("")
            print("Incorrect username entered.")
            time.sleep(.75)
            os.system("clear")
            if uthreshold == 9:
                print("")
                print("Last attempt before program terminates.")
                time.sleep(.75)
            elif (uthreshold == 10):
                print("")
                print("Terminating program...")
                os.system("clear")
                sys.exit()
                
    
        
            
