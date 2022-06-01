import mariadb
import datetime

conn = mariadb.connect(
    user="root",
    password="Arfarf123",
    host="localhost",
    database="tasklistingdb")
cur = conn.cursor() 


def addCategory():
    print("=========== ADD CATEGORY ===========")
    now  = datetime.date.today()
    categoryName = input("Please enter a category name: ")


    try: 
        cur.execute("INSERT INTO category (category_name, creation_date) VALUES (?, ?)", (categoryName,now))
    except mariadb.Error as e: 
        print(f"Error: {e}")
    
    finally:
            conn.commit()
            conn.close()


def editCategory():
    print("=========== EDIT CATEGORY ===========")
    findCategory = input("Enter the category name that you want to edit: ")

    try: 
        cur.execute("SELECT category_id FROM category WHERE category_name = ?", (findCategory,))
        result = cur.fetchone()
        if(result is not None):
            foundCategoryId = result[0]
            newCategory = input("Category found! Enter the new category name: ")

            cur.execute("UPDATE category SET category_name = ? WHERE category_id = ?", (newCategory, foundCategoryId,))   
            conn.commit()         
        else:
            print("Category not found!")

    except mariadb.Error as e: 
        print(f"Error: {e}")
    
    finally:
            conn.close()

def deleteCategory():
    print("=========== DELETE CATEGORY ===========")
    findCategory = input("Enter the category name that you want to delete: ")

    try: 
        cur.execute("SELECT category_id FROM category WHERE category_name = ?", (findCategory,))
        result = cur.fetchone()
        if(result is not None):
            foundCategoryId = result[0]

            cur.execute("DELETE FROM category WHERE category_id = ?", (foundCategoryId,))   
            conn.commit()

            print("Category deleted!")
        else:
            print("Category not found!")

    except mariadb.Error as e: 
        print(f"Error: {e}")
    
    finally:
            conn.close()

def viewCategory():
    print("=========== VIEW CATEGORY ===========")
    findCategory = input("Enter the category name that you want to view: ")

    try: 
        cur.execute("SELECT category_id FROM category WHERE category_name = ?", (findCategory,))
        result = cur.fetchone()
        if(result is not None):
            foundCategoryId = result[0]

            cur.execute("SELECT category_name, creation_date FROM category WHERE category_id = ?", (foundCategoryId,))
            categoryResult = cur.fetchone()

            print("Category name:", (categoryResult[0]))
            print("Category date:", (categoryResult[1]), "\n")

        else:
            print("Category not found!")

    except mariadb.Error as e: 
        print(f"Error: {e}")
    
    finally:
            conn.close()

def addTaskToCategory():
    print("=========== ADD TASK TO CATEGORY ===========")
    findTask = input("Enter the task name: ")

    try: 
        cur.execute("SELECT task_id FROM task WHERE task_name = ?", (findTask,))
        taskResult = cur.fetchone()
        if(taskResult is not None):

            findCategory = input("Enter the category: ")
            cur.execute("SELECT category_id FROM category WHERE category_name = ?", (findCategory,))
            categoryResult = cur.fetchone()
            if(categoryResult is not None):
                while True:
                    print("Category found! Do you want to add your task to this category?")
                    confirm = input("Y/N: ")
                    if(confirm == "N" or confirm == "n"):
                        print("Add-Task-To-Categiry stopped")
                        break
                    elif(confirm == "Y" or confirm == "y"):
                        cur.execute("UPDATE task SET category_id = ? WHERE task_id = ?", (taskResult[0], categoryResult[0]))
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
    
    finally:
            conn.close()
