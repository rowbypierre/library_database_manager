import sys, os, time 
from getpass import getpass

def logon():
    xusername = 'user'
    xpassword = 'password'
    status = "locked" 
    uthreshold = 0
    pthreshold = 0

    while status == "locked":
        username = input("\nEnter username: ").lower().strip()
        time.sleep(.75)
        uthreshold += 1
        if username == xusername:
            username = username.capitalize()
            print(f"\nWelcome {username}")
            time.sleep(.75)
            os.system("clear")
            
            while status == "locked":
                password = getpass("\nEnter password: ").lower().strip()
                time.sleep(.75)
                pthreshold += 1
                if password == xpassword:
                    print(f"\nCorrect password entered for username: {username}")
                    time.sleep(.75)
                    status = "unlocked"
                    os.system("clear")
                else:
                    
                    if pthreshold == 9:
                        print("\nLast attempt before program terminates.")
                        time.sleep(.75)
                        os.system("clear")
                    if pthreshold in range (1, 8):
                        print("\nIncorrect password entered for: " + username)
                        time.sleep(.75)
                        os.system("clear")
                    elif pthreshold == 10:
                        print("\nTerminating program...")
                        os.system("clear")
                        sys.exit()
                        
        else: 
            print("\nIncorrect username entered.")
            time.sleep(.75)
            os.system("clear")
            if uthreshold == 9:  
                print("\nLast attempt before program terminates.")
                time.sleep(.75)
            elif (uthreshold == 10):
                print("\nTerminating program...")
                os.system("clear")
                sys.exit()
                
    
        
            
