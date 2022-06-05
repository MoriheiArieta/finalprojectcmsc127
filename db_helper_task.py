import mariadb
import datetime
import re

# INTIAL SECTION

# connecting to the root user first and check if the 'tasklistingdb' database exist
connInit = mariadb.connect(user="root", password="Arfarf123", host="localhost")

curInit = connInit.cursor()

# function to check whether or not 'tasklistingdb' database exist. If it doesn't exist, it should create the databases along with its tables
def databaseExist():
    try:
        curInit.execute("SHOW DATABASES")
        dbList = curInit.fetchall()
        databaseName = "tasklistingdb"

        # Scenario 1: Database exist
        if (databaseName,) in dbList:
            print("Database found...")

        # Scenario 2: Database does not exist. Thus, create the database with its tables
        else:
            print("Database not found. Creating 'tasklistingdb' database...")
            curInit.execute("CREATE DATABASE {}".format(databaseName))

            # conn = mariadb.connect(
            #     user="root",
            #     password="macmac924",
            #     host="localhost",
            #     database=databaseName,
            # )

            # cur = conn.cursor()

            conn = mariadb.connect(
                user="root",
                password="Arfarf123",
                host="localhost",
                database=databaseName,
            )

            cur = conn.cursor()

            userTable = """CREATE TABLE user(
                    user_id INT AUTO_INCREMENT,
                    username VARCHAR(20) NOT NULL,
                    password VARCHAR(15) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    CONSTRAINT user_user_id_pk PRIMARY KEY (user_id),
                    CONSTRAINT user_username_uk UNIQUE KEY (username),
                    CONSTRAINT user_email_uk UNIQUE KEY (email)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3
                    """

            categoryTable = """CREATE TABLE category(
                    category_id INT AUTO_INCREMENT,
                    category_name VARCHAR(15),
                    creation_date DATE,
                    user_id INT,
                    CONSTRAINT category_user_id_fk FOREIGN KEY (user_id) REFERENCES user(user_id),
                    CONSTRAINT category_category_id_pk PRIMARY KEY (category_id),
                    CONSTRAINT category_category_name_uk UNIQUE KEY (category_name)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
                    """

            taskTable = """CREATE TABLE task(
                    task_id INT AUTO_INCREMENT,
                    task_name VARCHAR(255),
                    task_details VARCHAR(255),
                    task_date DATE,
                    task_completed VARCHAR(10),
                    user_id INT,
                    category_id INT,
                    CONSTRAINT task_task_id_pk PRIMARY KEY (task_id),
                    CONSTRAINT task_user_id_fk FOREIGN KEY (user_id) REFERENCES user(user_id),
                    CONSTRAINT task_category_id_fk FOREIGN KEY (category_id) REFERENCES category(category_id),
                    CONSTRAINT task_task_name_uk UNIQUE KEY (task_name)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
                    """
            cur.execute(userTable)
            conn.commit()
            cur.execute(categoryTable)
            conn.commit()
            cur.execute(taskTable)
            conn.commit()
            conn.close()

    except mariadb.Error as e:
        print(f"Error: {e}")

    finally:
        connInit.close()


# function call
databaseExist()


conn = mariadb.connect(
    user="root", password="Arfarf123", host="localhost", database="tasklistingdb"
)
cur = conn.cursor()


# USER SECTION


# function for adding data to tasklistingdb.user
def addUser():
    print("\n=========== SIGN-UP ===========")

    email = input("Please enter your email: ")

    # email format validation
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    if re.fullmatch(regex, email):
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")

        try:
            cur.execute("SELECT user_id FROM user WHERE username = ?", (username,))
            usernameResult = cur.fetchone()
            cur.execute("SELECT user_id FROM user WHERE email = ?", (email,))
            emailResult = cur.fetchone()

            if usernameResult is not None:
                print("Username already exists! Please use another username")
                return False
            elif emailResult is not None:
                print("Email already exists! Please use another email")
                return False
            else:
                loop = True
                while loop:
                    rePassword = input("Please re-type your password: ")
                    if password != rePassword:
                        print("Please match your password")
                    else:
                        cur.execute(
                            "INSERT INTO user (username, password, email) VALUES (?, ?, ?)",
                            (username, password, email),
                        )
                        loop = False
                        conn.commit()
                        return True
        except mariadb.Error as e:
            print(f"Error: {e}")
            return False
    else:
        print("Invalid Email")
        return False


# function for checking registered users/logging in
def userLogin():
    cur.execute("SELECT * FROM user")
    userResult = cur.fetchone()
    if userResult is None:
        print("No users yet!")
        return False
    else:
        print("=========== LOG-IN ===========")

        email = input("Please enter your email: ")
        password = input("Please enter your password: ")

        try:

            cur.execute(
                "SELECT user_id, username FROM user WHERE email = ? AND password = ?",
                (email, password),
            )
            result = cur.fetchone()
            if result is not None:
                return result
            else:
                print("User not found! Please make sure you have an account")
                return False

        except mariadb.Error as e:
            print(f"Error: {e}")


# CATEGORY SECTION

# function for adding category/data to taskinglistdb.category
def addCategory(userId):
    print("=========== ADD CATEGORY ===========")
    now = datetime.date.today()
    categoryName = input("Please enter a category name: ")

    try:
        cur.execute(
            "SELECT category_id FROM category WHERE category_name = ?", (categoryName,)
        )
        categoryResult = cur.fetchone()
        if categoryResult is not None:
            print("Category already exists! Please enter another category name")
        else:
            cur.execute(
                "INSERT INTO category (category_name, creation_date, user_id) VALUES (?, ?, ?)",
                (categoryName, now, userId),
            )
            conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")


# function for updating data from taskinglistdb.category
def editCategory(userId):
    cur.execute("SELECT * FROM category WHERE user_id = ?", (userId,))
    categoryResult = cur.fetchone()
    if categoryResult is None:
        print("No categories yet!")
    else:
        print("=========== EDIT CATEGORY ===========")
        findCategory = input("Enter the category name that you want to edit: ")

        try:
            cur.execute(
                "SELECT category_id FROM category WHERE category_name = ?",
                (findCategory,),
            )
            result = cur.fetchone()
            if result is not None:
                foundCategoryId = result[0]
                newCategory = input("Category found! Enter the new category name: ")

                cur.execute(
                    "UPDATE category SET category_name = ? WHERE category_id = ?",
                    (
                        newCategory,
                        foundCategoryId,
                    ),
                )
                conn.commit()
            else:
                print("Category not found!")

        except mariadb.Error as e:
            print(f"Error: {e}")


# function for deleting category/data from taskinglistdb.category
def deleteCategory(userId):
    cur.execute("SELECT * FROM category WHERE user_id = ?", (userId,))
    categoryResult = cur.fetchone()
    if categoryResult is None:
        print("No categories yet!")
    else:

        print("=========== DELETE CATEGORY ===========")
        findCategory = input("Enter the category name that you want to delete: ")

        try:
            cur.execute(
                "SELECT category_id FROM category WHERE category_name = ?",
                (findCategory,),
            )
            result = cur.fetchone()
            if result is not None:
                foundCategoryId = result[0]

                cur.execute(
                    "DELETE FROM category WHERE category_id = ?", (foundCategoryId,)
                )
                conn.commit()

                print("Category deleted!")
            else:
                print("Category not found!")

        except mariadb.Error as e:
            print(f"Error: {e}")


# function for viewing data from taskinglistdb.category
def viewCategory(userId):
    cur.execute("SELECT * FROM category WHERE user_id = ?", (userId,))
    categoryResult = cur.fetchone()
    if categoryResult is None:
        print("No categories yet!")
    else:
        print("=========== VIEW CATEGORY ===========")
        findCategory = input("Enter the category name that you want to view: ")

        try:
            cur.execute(
                "SELECT category_id FROM category WHERE category_name = ?",
                (findCategory,),
            )
            result = cur.fetchone()
            if result is not None:
                foundCategoryId = result[0]

                cur.execute(
                    "SELECT category_name, creation_date FROM category WHERE category_id = ?",
                    (foundCategoryId,),
                )
                categoryResult = cur.fetchone()

                print("Category name:", (categoryResult[0]))
                print("Category date:", (categoryResult[1]))

            else:
                print("Category not found!")

        except mariadb.Error as e:
            print(f"Error: {e}")


# function for categorizing a task
def addTaskToCategory(userId):
    cur.execute("SELECT * FROM category WHERE user_id = ?", (userId,))
    categoryResult = cur.fetchone()
    cur.execute("SELECT * FROM task WHERE user_id = ?", (userId,))
    taskResult = cur.fetchone()
    if categoryResult is None:
        print("No categories yet!")
    elif taskResult is None:
        print("No tasks yet!")
    else:
        print("=========== ADD TASK TO CATEGORY ===========")
        findTask = input("Enter the task name: ")

        try:
            cur.execute("SELECT task_id FROM task WHERE task_name = ?", (findTask,))
            taskResult = cur.fetchone()
            if taskResult is not None:

                findCategory = input("Enter the category: ")
                cur.execute(
                    "SELECT category_id FROM category WHERE category_name = ?",
                    (findCategory,),
                )
                categoryResult = cur.fetchone()
                if categoryResult is not None:
                    while True:
                        print(
                            "Category found! Do you want to add your task to this category?"
                        )
                        confirm = input("Y/N: ")
                        if confirm == "N" or confirm == "n":
                            print("Add-Task-To-Categiry stopped")
                            break
                        elif confirm == "Y" or confirm == "y":
                            cur.execute(
                                "UPDATE task SET category_id = ? WHERE task_id = ?",
                                (taskResult[0], categoryResult[0]),
                            )
                            conn.commit()
                            print("Successfully inserted Task to Category!")
                            break
                        else:
                            print("Invalid output. Y/N?")
                else:
                    print("Category not found!")
            else:
                print("Task not found!")

        except mariadb.Error as e:
            print(f"Error: {e}")


# TASK SECTION

# function for adding task/data to taskinglistdb.task
def addTask(userId):
    print("=========== CREATE TASK ===========")
    now = datetime.date.today()
    taskName = input("Please enter a task name: ")
    taskDetails = input("Please enter your task details: ")

    try:
        cur.execute("SELECT task_id FROM task WHERE task_name = ?", (taskName,))
        taskResult = cur.fetchone()
        if taskResult is not None:
            print("Task name already exists! Please enter another task name")
        else:
            cur.execute(
                "INSERT INTO task (task_name, task_details, task_date, task_completed, user_id) VALUES (?, ?, ?, ?, ?)",
                (taskName, taskDetails, now, "No", userId),
            )
            conn.commit()
            print("Successfully created Task!")
    except mariadb.Error as e:
        print(f"Error: {e}")


# function for updating data from taskinglistdb.task
def editTask(userId):
    cur.execute("SELECT * FROM task WHERE user_id = ?", (userId,))
    taskResult = cur.fetchone()
    if taskResult is None:
        print("No tasks yet!")
    else:
        print("=========== EDIT TASK ===========")
        findTask = input("Enter the task name that you want to edit: ")

        try:
            cur.execute("SELECT task_id FROM task WHERE task_name = ?", (findTask,))
            result = cur.fetchone()
            if result is not None:
                foundTaskId = result[0]
                newTaskName = input("Task found! Enter the new task name: ")
                newTaskDetails = input("Enter the new task details: ")

                cur.execute(
                    "UPDATE task SET task_name = ?, task_details = ? WHERE task_id = ?",
                    (newTaskName, newTaskDetails, foundTaskId),
                )
                conn.commit()
                print("Successfully edited Task!")
            else:
                print("Task not found!")

        except mariadb.Error as e:
            print(f"Error: {e}")


# function for deleting task/data from taskinglistdb.task
def deleteTask(userId):
    cur.execute("SELECT * FROM task WHERE user_id = ?", (userId,))
    taskResult = cur.fetchone()
    if taskResult is None:
        print("No tasks yet!")
    else:
        print("=========== DELETE TASK ===========")
        findTask = input("Enter the task name that you want to delete: ")

        try:
            cur.execute("SELECT task_id FROM task WHERE task_name = ?", (findTask,))
            result = cur.fetchone()
            if result is not None:
                foundTaskId = result[0]

                cur.execute("DELETE FROM task WHERE task_id = ?", (foundTaskId,))
                conn.commit()

                print("Task deleted!")
            else:
                print("Task not found!")

        except mariadb.Error as e:
            print(f"Error: {e}")


# function for updating task_completed from taskinglistdb.task
def markTaskDone(userId):
    cur.execute("SELECT * FROM task WHERE user_id = ?", (userId,))
    taskResult = cur.fetchone()
    if taskResult is None:
        print("No tasks yet!")
    else:
        print("=========== MARK TASK AS DONE ===========")
        findTask = input("Enter the task name that you want to mark as done: ")

        try:
            cur.execute(
                "SELECT task_id FROM task WHERE task_name = ? AND task_completed = 'No'",
                (findTask,),
            )
            result = cur.fetchone()
            if result is not None:
                foundTaskId = result[0]

                cur.execute(
                    "UPDATE task SET task_completed = 'Yes' WHERE task_id = ?",
                    (foundTaskId,),
                )
                conn.commit()

                print("Task marked as done!")
            else:
                print("Task not found or it has already been completed!")

        except mariadb.Error as e:
            print(f"Error: {e}")


# function for viewing all data from taskinglistdb.task
def viewAllTasks(userId):
    cur.execute("SELECT * FROM task WHERE user_id = ?", (userId,))
    taskResult = cur.fetchone()
    if taskResult is None:
        print("No tasks yet!")
    else:
        print("=========== VIEW ALL TASKS ===========")
        try:
            cur.execute("SELECT * FROM task WHERE user_id = ?", (userId,))

            allTasks = cur.fetchall()
            if allTasks is not None:
                for index, task in enumerate(allTasks, start=1):
                    print("{}.".format(index))
                    print("Task name: {}".format(task[1]))
                    print("Task details: {}".format(task[2]))
                    print("Created date: {}".format(task[3]))
                    print("Completed: {}".format(task[4]))

                    cur.execute(
                        "SELECT category_name FROM category WHERE category_id = ?",
                        (task[6],),
                    )
                    categoryName = cur.fetchone()
                    if categoryName is not None:
                        print("Category name: {}".format(categoryName[0]))
                    else:
                        print("Category name: None")
                    print("")
        except mariadb.Error as e:
            print(f"Error: {e}")


# close connection to the database
def closeDatabase():
    conn.close()