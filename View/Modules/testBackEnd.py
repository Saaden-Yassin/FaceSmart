from Controller.ManagerCRUD import *
from Controller.ScheduleCRUD import *
from Model.Schedule import *


# region TestManagerClass
# region Function to create a manager
def create_manager():
    firstName = input("Enter first name: ")
    lastName = input("Enter last name: ")
    username = input("Enter username: ")
    age = int(input("Enter age: "))
    email = input("Enter email: ")
    image = input("Enter image: ")
    password = input("Enter password: ")
    manager = Manager(firstName=firstName, lastName=lastName, username=username, age=age, email=email, image=image,
                      password=password)
    if createManager(manager):
        print("Manager created successfully!")
    else:
        print("Failed to create manager.")


# endregion

# region Function to delete a manager
def delete_manager():
    manager_id = int(input("Enter manager ID to delete: "))
    deleteManager(ID=manager_id)
    print("Manager deleted successfully!")


# endregion

# region Function to update a manager
def update_manager():
    manager_id = int(input("Enter manager ID to update: "))
    print("Enter new manager details (leave blank to keep current values):")
    firstName = input("Enter new first name: ")
    lastName = input("Enter new last name: ")
    username = input("Enter new username: ")
    age = int(input("Enter new age: ")) if input("Update age? (y/n): ").lower() == 'y' else None
    email = input("Enter new email: ")
    image = input("Enter new image: ")
    password = input("Enter new password: ")
    updateManager(ID=manager_id, firstName=firstName, lastName=lastName, username=username, age=age, email=email,
                  image=image, password=password)
    print("Manager updated successfully!")


# endregion

# region Function to get all managers
def get_all_managers():
    managers = getAllManagers()
    if managers:
        print("Managers:")
        for manager in managers:
            print(manager)
    else:
        print("No managers found.")


# endregion

# region Main menu function
def manager_operations():
    while True:
        print("\nOptions:")
        print("1. Create Manager")
        print("2. Delete Manager")
        print("3. Update Manager")
        print("4. Get All Managers")
        print("q. Quit")
        Mchoice = input("Enter your choice: ").lower()
        if Mchoice == '1':
            create_manager()
        elif Mchoice == '2':
            delete_manager()
        elif Mchoice == '3':
            update_manager()
        elif Mchoice == '4':
            get_all_managers()
        elif Mchoice == 'q':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


# endregion

# endregion

# region TestClassEmployee

# Function to create an employee
def create_employee():
    firstName = input("Enter first name: ")
    lastName = input("Enter last name: ")
    age = int(input("Enter age: "))
    email = input("Enter email: ")
    image = input("Enter image: ")
    departmentName = input("Enter department name: ")
    projectName = input("Enter project name: ")
    employee = Employee(firstName=firstName, lastName=lastName, age=age, email=email, image=image,
                        departmentName=departmentName, projectName=projectName)
    if createEmployee(employee):
        print("Employee created successfully!")
    else:
        print("Failed to create employee.")


# Function to delete an employee
def delete_employee():
    employee_id = int(input("Enter employee ID to delete: "))
    deleteEmployee(ID=employee_id)
    print("Employee deleted successfully!")


# Function to update an employee
def update_employee():
    employee_id = int(input("Enter employee ID to update: "))
    print("Enter new employee details (leave blank to keep current values):")
    firstName = input("Enter new first name: ")
    lastName = input("Enter new last name: ")
    age = int(input("Enter new age: ")) if input("Update age? (y/n): ").lower() == 'y' else None
    email = input("Enter new email: ")
    image = input("Enter new image: ")
    departmentName = input("Enter new department name: ")
    projectName = input("Enter new project name: ")
    updateEmployee(ID=employee_id, firstName=firstName, lastName=lastName, age=age, email=email, image=image,
                   departmentName=departmentName, projectName=projectName)
    print("Employee updated successfully!")


# Function to read employee details
def read_employee():
    employee_id = int(input("Enter employee ID to read: "))
    employee = getEmployeeById(ID=employee_id)
    if employee:
        print("Employee details:")
        print(employee[0])
    else:
        print("Employee not found.")


# Main function to perform employee operations
def employee_operations():
    options = {
        '1': create_employee,
        '2': delete_employee,
        '3': update_employee,
        '4': read_employee,
        'q': lambda: None  # Quit function
    }
    while True:
        print("\nOptions:")
        print("1. Create Employee")
        print("2. Delete Employee")
        print("3. Update Employee")
        print("4. Read Employee")
        print("q. Quit")
        choice = input("Enter your choice: ").lower()
        if choice in options:
            if choice == 'q':
                print("Exiting...")
                break
            options[choice]()
        else:
            print("Invalid choice. Please try again.")


# endregion

# region TestClassProject

# Function to create a project
def create_project():
    name = input("Enter project name: ")
    startDate = input("Enter start date (YYYY-MM-DD): ")
    endDate = input("Enter end date (YYYY-MM-DD): ")
    status = input("Enter status: ")
    employeesIDs = input("Enter comma-separated employee IDs: ").split(',')
    project = Project(name=name, startDate=startDate, endDate=endDate, status=status,
                      employeesIDsList=list(map(int, employeesIDs)))
    createProject(project)


# Function to get all projects
def get_all_projects():
    projects = getProjects()
    if projects:
        print("Projects:")
        for project in projects:
            print(project)
    else:
        print("No projects found.")


# Function to update a project
def update_project():
    project_id = int(input("Enter project ID to update: "))
    name = input("Enter new project name (leave blank to keep current value): ")
    startDate = input("Enter new start date (YYYY-MM-DD) (leave blank to keep current value): ")
    endDate = input("Enter new end date (YYYY-MM-DD) (leave blank to keep current value): ")
    status = input("Enter new status (leave blank to keep current value): ")
    employeesIDs = input("Enter comma-separated new employee IDs (leave blank to keep current value): ")
    if employeesIDs:
        employeesIDs = employeesIDs.split(',')
    updateProject(ID=project_id, name=name, startDate=startDate, endDate=endDate, status=status,
                  employeesIDsList=employeesIDs)


# Function to delete a project
def delete_project():
    project_id = int(input("Enter project ID to delete: "))
    deleteProject(ID=project_id)
    print("Project deleted successfully!")


# Main menu function for project operations
def project_operations():
    while True:
        print("\nOptions:")
        print("1. Create Project")
        print("2. Get All Projects")
        print("3. Update Project")
        print("4. Delete Project")
        print("q. Quit")
        choice = input("Enter your choice: ").lower()
        if choice == '1':
            create_project()
        elif choice == '2':
            get_all_projects()
        elif choice == '3':
            update_project()
        elif choice == '4':
            delete_project()
        elif choice == 'q':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


# endregion

# region TestClassSchedule

# Function to create a schedule
def create_schedule():
    try:
        employee_id = int(input("Enter employee ID: "))
        image = input("Enter employee image: ")
        schedule = Schedule(employeeImage=image,
                            checkDay=datetime.now().strftime("%Y-%m-%d"),
                            beginningTime=datetime.now().strftime("%H:%M:%S"))
        if createSchedule(schedule):
            print("Schedule created successfully!")
        else:
            print("Failed to create schedule.")
    except ValueError:
        print("Invalid input! Please enter a valid employee ID.")


# Function to get all schedules
def get_all_schedules():
    schedules = getSchedules()
    if schedules:
        print("Schedules:")
        for schedule in schedules:
            print(schedule)
    else:
        print("No schedules found.")


# Function to update a schedule
def update_schedule():
    try:
        employee_id = int(input("Enter employee ID to update schedule: "))
        if updateSchedule(employeeID=employee_id):
            print("Schedule updated successfully!")
        else:
            print("Failed to update schedule.")
    except ValueError:
        print("Invalid input! Please enter a valid employee ID.")


# Function to delete a schedule
def delete_schedule():
    try:
        schedule_id = int(input("Enter schedule ID to delete: "))
        deleteSchedule(ID=schedule_id)
        print("Schedule deleted successfully!")
    except ValueError:
        print("Invalid input! Please enter a valid schedule ID.")


# Function to check in
def check_in():
    image = input("Enter employee image for check-in: ")
    if checkIn(image=image):
        print("Check-in successful! ")
        print("Number of Employees: ", getTotalNumberOfEmployees())
        print("Number of Active Employees: ", getNumberEmployeesActive())
        print("Number of Inactive Employees: ", getNumberEmployeesInactive())
    else:
        print("Check-in failed.")


# Function to check out
def check_out():
    image = input("Enter employee image for check-out: ")
    if checkOut(image=image):
        print("Check-out successful!")
        print("Number of Employees: ", getTotalNumberOfEmployees())
        print("Number of Active Employees: ", getNumberEmployeesActive())
        print("Number of Inactive Employees: ", getNumberEmployeesInactive())
    else:
        print("Check-out failed.")


# Main menu function for schedule operations
def schedule_operations():
    while True:
        print("\nOptions:")
        print("1. Create Schedule")
        print("2. Get All Schedules")
        print("3. Update Schedule")
        print("4. Delete Schedule")
        print("5. Check-In")
        print("6. Check-Out")
        print("q. Quit")
        choice = input("Enter your choice: ").lower()
        if choice == '1':
            create_schedule()
        elif choice == '2':
            get_all_schedules()
        elif choice == '3':
            update_schedule()
        elif choice == '4':
            delete_schedule()
        elif choice == '5':
            check_in()
        elif choice == '6':
            check_out()
        elif choice == 'q':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


# endregion


def main():
    while True:
        print("\nOptions:")
        print("1. Manager Operations")
        print("2. Employee Operations")
        print("3. Project Operations")
        print("4. Schedule Operations")
        print("q. Quit")

        choice = input("Enter your choice: ").lower()

        if choice == '1':
            manager_operations()
        elif choice == '2':
            employee_operations()
        elif choice == '3':
            project_operations()
        elif choice == '4':
            schedule_operations()
        elif choice == 'q':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


main()
