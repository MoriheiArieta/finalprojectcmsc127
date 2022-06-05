from db_helper_task import *

# function for showing main menu
def showMenu(User):
    userId = User[0]
    userName = User[1]

    loop = True
    while loop:
        print("=========== What would you like to do, {}? ===========".format(userName))
        print("[1] Add task")
        print("[2] Edit task")
        print("[3] Delete task")
        print("[4] View all tasks")
        print("[5] Mark task as done")
        print("[6] Add category")
        print("[7] Delete category")
        print("[8] View category")
        print("[9] Add task to category")
        print("[0] Log-out")

        choice = input("Enter choice: ")
        if choice.isnumeric() == False:
            print("Please enter a valid integer!\n")
        else:
            val = int(choice)
            if val < 0 or val > 9:
                print("Please enter a valid choice!\n")
            else:
                if val == 1:
                    addTask(userId)
                elif val == 2:
                    editTask(userId)
                elif val == 3:
                    deleteTask(userId)
                elif val == 4:
                    viewAllTasks(userId)
                elif val == 5:
                    markTaskDone(userId)
                elif val == 6:
                    addCategory(userId)
                elif val == 7:
                    deleteCategory(userId)
                elif val == 8:
                    viewCategory(userId)
                elif val == 9:
                    addTaskToCategory(userId)
                elif val == 0:
                    return False


# function for showing user login/signup menu
def showUserPage():
    loop = True
    while loop:
        print("\n=========== WELCOME TO THE TASK LISTER APP ===========")
        print("[1] Log-in")
        print("[2] Sign-up")
        print("[0] Shut-down Application")

        choice = input("Enter choice: ")
        if choice.isnumeric() == False:
            print("Please enter a valid integer!\n")
        else:
            val = int(choice)
            if val < 0 or val > 2:
                print("Please enter a valid choice!\n")
            elif val == 1:
                check = userLogin()
                if check == False:
                    loop = True
                else:
                    print("User found! Redirecting to the application...")
                    menu = showMenu(check)
                    if menu == False:
                        loop = True
                    else:
                        loop = True
            elif val == 2:
                check = addUser()
                if check == False:
                    print("Sign-up not successful!")
                else:
                    print("Sign-up successful!")
            else:
                print("Goodbye!\n")
                closeDatabase()
                loop = False


# Main Section
showUserPage()


# References:
#   MySQL implementation in Python: https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
#   MySQL Connector/Python Developer Guide: https://dev.mysql.com/doc/connector-python/en/
#   Indexing while printing tuples: https://stackoverflow.com/a/23886515
#   RegEx email validation:         https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
