import sys, os, time 
from getpass import getpass

def logon():
    xusername = 'user'
    xpassword = 'password'
    status = "locked" 
    uthreshold = 0
    pthreshold = 0

    while status == "locked":
        username = input("\n Enter username: ").lower().strip()
        time.sleep(.75)
        uthreshold += 1
        if username == xusername:
            username = username.capitalize()
            print(f"\n Welcome {username}")
            time.sleep(.75)
            os.system("clear")
            
            while status == "locked":
                password = getpass("\n Enter password: ").lower().strip()
                time.sleep(.75)
                pthreshold += 1
                if password == xpassword:
                    print(f"\n Correct password entered for username: {username}")
                    time.sleep(.75)
                    status = "unlocked"
                    os.system("clear")
                else:
                    
                    if pthreshold == 9:
                        print("\n Last attempt before program terminates.")
                        time.sleep(.75)
                        os.system("clear")
                    if pthreshold in range (1, 8):
                        print("\n Incorrect password entered for: " + username)
                        time.sleep(.75)
                        os.system("clear")
                    elif pthreshold == 10:
                        print("\n Terminating program...")
                        os.system("clear")
                        sys.exit()
                        
        else: 
            print("\n Incorrect username entered.")
            time.sleep(.75)
            os.system("clear")
            if uthreshold == 9:  
                print("\n Last attempt before program terminates.")
                time.sleep(.75)
            elif (uthreshold == 10):
                print("\n Terminating program...")
                os.system("clear")
                sys.exit()
                
    
        
            
