def showMenu ():
    
    while True:
        print("WELCOME TO TASK LISTER!")
        print("[1] Add task")
        print("[2] Edit task")
        print("[3] Delete task")
        print("[4] View task")
        print("[5] Mark task")

        print("[6] Add category")
        print("[7] Delete category")
        print("[8] View category")
        print("[9] Add task to category")
        print("[0] Exit program")
        
        try:
            choice = int(input("What would you like to do?: "))
        except ValueError:    
            print("!!!Please enter a valid selection!!!\n")
        else:
            if choice != 0:
                print("!!!Please enter a valid selection!!!\n")


showMenu()