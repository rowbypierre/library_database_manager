import sys 

status = "locked" 
uthreshold = 0
pthreshold = 0

while status == "locked":
    
    username = input("Enter username: ").lower().strip()
    uthreshold += 1
    
    if uthreshold == 9:
        print("Last attempt before script terminates.")
    elif (uthreshold == 10) and (username != "test"):
        print("Terminating script...")
        sys.exit()
    elif username == "test":
        prompt = f"Welcome {username}"
        print(prompt.lower())
        
        while status == "locked":
            
            password = input("Enter password: ").lower().strip()
            pthreshold += 1
            
            if (pthreshold == 9):
                print("Last attempt before script terminates.")
            elif pthreshold == 10 and (password != "password"):
                print("Terminating script...")
                sys.exit()
            elif password == "password":
                prompt = f"Correct password entered for username: {username}"
                status = "unlocked"
                
print("REST OF THE CODE")



