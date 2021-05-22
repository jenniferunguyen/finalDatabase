import mysql.connector
from faker import Faker
import csv
from datetime import date
import random
from random import randrange
import distutils
from distutils import util
import os.path
import logGenerator


db = mysql.connector.connect(
    host="34.94.78.23",
    user="IamRene",
    passwd="40*GermaN",
    database="Final"
)

# GENERATE FAKE DATA
fake = Faker()

states = ['CA', 'OR', 'WA']
preferences = ['cat', 'dog']
phases = ['fostering', 'adopting']
genders = ['female', 'male']

# generate clients data
def genClients(num: int):
    csv_file = open("./clients.csv", "w", newline='')
    writer = csv.writer(csv_file)
    writer.writerow(["FirstName","LastName","DOB","Phone","Email",
                     "Address","City","State","Zip",
                     "Occupation","Preference","Phase",
                     "Approved?","Update"])
    for x in range(0, num):
        writer.writerow([fake.first_name(),
                        fake.last_name(),
                        fake.date_between_dates(date_start=date(1970, 1, 1), date_end=date(2004, 1, 1)),
                        fake.numerify('###-###-####'),
                        fake.email(),
                        fake.street_address(),
                        fake.city(),
                        random.choice(states),
                        fake.pyint(min_value=90000, max_value=99500),
                        fake.job(),
                        random.choice(preferences),
                        random.choice(phases),
                        fake.boolean(),
                        fake.date_between_dates(date_start=date(2000, 1, 1), date_end=date(2004, 1, 1))])

# generate pets data
def genPets(num: int):
    csv_file = open("./pets.csv", "w", newline='')
    writer = csv.writer(csv_file)
    writer.writerow(["Name", "DOB", "Gender",
                     "Type", "HealthConcerns",
                     "Phase"])
    for x in range(0, num):
        writer.writerow([fake.first_name(),
                        fake.date_between_dates(date_start=date(1991, 1, 1), date_end=date(2021, 1, 1)),
                        random.choice(genders),
                        random.choice(preferences),
                        fake.boolean(),
                        random.choice(phases)])

# generate shelters data
def genShelters(num: int):
    csv_file = open("./shelters.csv", "w", newline='')
    writer = csv.writer(csv_file)
    writer.writerow(["Phone","Email",
                     "Address","City","State","Zip"])
    for x in range(0, num):
        writer.writerow([fake.numerify('###-###-####'),
                        fake.last_name().lower()+"@pawsibleshelters.com",
                        fake.street_address(),
                        fake.city(),
                        random.choice(states),
                        fake.pyint(min_value=90000, max_value=99500)])

# generate employees data
def genEmployees(num: int):
    csv_file = open("./employees.csv", "w", newline='')
    writer = csv.writer(csv_file)
    writer.writerow(["FirstName","LastName","DOB","Phone","Email",
                     "Address","City","State","Zip"])
    for x in range(0, num):
        writer.writerow([fake.first_name(),
                        fake.last_name(),
                        fake.date_between_dates(date_start=date(1970, 1, 1), date_end=date(2004, 1, 1)),
                        fake.numerify('###-###-####'),
                        fake.email(),
                        fake.street_address(),
                        fake.city(),
                        random.choice(states),
                        fake.pyint(min_value=90000, max_value=99500)])

# IMPORT DATA
def importDatạ():
    mycursor = db.cursor()
    # fill Clients table
    try:
        with open("./clients.csv") as csv_file:
            reader = csv.DictReader(csv_file)
            print("Importing clients...")
            clientCount = 0
            for row in reader:
                mycursor.execute("INSERT INTO Clients(FirstName, LastName, DateOfBirth, Phone, Email, "
                                 "Address, City, State, Zip,"
                                 "Occupation, Preference, Phase,"
                                 "Status, StatusDate)"
                                 "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                                 (row["FirstName"], row["LastName"], row["DOB"], row["Phone"], row["Email"],
                                  row["Address"], row["City"], row["State"], row["Zip"],
                                  row["Occupation"], row["Preference"], row["Phase"],
                                  distutils.util.strtobool(row["Approved?"]), row["Update"]))
                db.commit()
                clientCount += 1
    except KeyError:
        print("ERROR in clients.csv. Make sure the columns are labeled appropriately.")
        db.rollback()
        exit()
    except mysql.connector.Error as error:
        print("ERROR: Use createTables.sql to create the Clients table.")
        exit()
    # fill Pets table
    try:
        with open("./pets.csv") as csv_file:
            reader = csv.DictReader(csv_file)
            print("Importing pets...")
            petCount = 0
            for row in reader:
                mycursor.execute("INSERT INTO Pets(Name, DateOfBirth, Gender,"
                                 "Type, HealthConcerns, Phase)"
                                 "VALUES (%s,%s,%s,%s,%s,%s);",
                                 (row["Name"], row["DOB"], row["Gender"],
                                  row["Type"], distutils.util.strtobool(row["HealthConcerns"]), row["Phase"]))
                db.commit()
                petCount += 1
    except KeyError:
        print("ERROR in pets.csv. Make sure the columns are labeled appropriately.")
        print("You should clear the Clients table before trying again.")
        db.rollback()
        exit()
    except mysql.connector.Error as error:
        print("ERROR: Use createTables.sql to create the Pets table.")
        print("You should clear the Clients table before trying again.")
        exit()
    # fill Shelters table
    try:
        with open("./shelters.csv") as csv_file:
            reader = csv.DictReader(csv_file)
            print("Importing shelters...")
            shelterCount = 0
            for row in reader:
                mycursor.execute("INSERT INTO Shelters(Phone, Email, "
                                 "Address, City, State, Zip)"
                                 "VALUES (%s,%s,%s,%s,%s,%s);",
                                 (row["Phone"], row["Email"],
                                  row["Address"], row["City"], row["State"], row["Zip"]))
                db.commit()
                shelterCount += 1
    except KeyError:
        print("ERROR in shelters.csv. Make sure the columns are labeled appropriately.")
        print("You should clear the Clients table and Pets table before trying again.")
        db.rollback()
        exit()
    except mysql.connector.Error as error:
        print("ERROR: Use createTables.sql to create the Shelters table.")
        print("You should clear the Clients table and Pets table before trying again.")
        exit()
    # fill Employees table
    try:
        with open("./employees.csv") as csv_file:
            reader = csv.DictReader(csv_file)
            print("Importing employees...")
            employeeCount = 0
            for row in reader:
                mycursor.execute("INSERT INTO Employees(FirstName, LastName, DateOfBirth, Phone, Email, "
                                 "Address, City, State, Zip)"
                                 "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                                 (row["FirstName"], row["LastName"], row["DOB"], row["Phone"], row["Email"],
                                  row["Address"], row["City"], row["State"], row["Zip"]))
                db.commit()
                employeeCount += 1
    except KeyError:
        print("ERROR in employees.csv. Make sure the columns are labeled appropriately.")
        print("You should clear the Clients table, Pets table, and Shelters table before trying again.")
        db.rollback()
        exit()
    except mysql.connector.Error as error:
        print("ERROR: Use createTables.sql to create the Employees table.")
        print("You should clear the Clients table, Pets table, and Shelters table before trying again.")
        exit()
    # fill ClientToEmployee table
    for i in range(1, clientCount+1):
        mycursor.execute("INSERT INTO ClientToEmployee(ClientID,EmployeeID)"
                        "VALUES (%s,%s);",
                        (i, randrange(1, employeeCount+1)))
        db.commit()
    # fill PetToShelter table
    for i in range(1, petCount+1):
        mycursor.execute("INSERT INTO PetToShelter(petID,shelterID)"
                        "VALUES (%s,%s);",
                        (i, randrange(1, shelterCount+1)))
        db.commit()
    # fill EmployeeToShelter table
    for i in range(1, employeeCount+1):
        mycursor.execute("INSERT INTO EmployeeToShelter(employeeID,shelterID)"
                        "VALUES (%s,%s);",
                        (i, randrange(1, shelterCount+1)))
        db.commit()
    # generate log data
    logGenerator.run()
    mycursor.close()
    db.close()


# USER INPUT

print("Welcome to the")
print(" ____        _           ____                           _             ")
print("|  _ \  __ _| |_ __ _   / ___| ___ _ __   ___ _ __ __ _| |_ ___  _ __ ")
print("| | | |/ _` | __/ _` | | |  _ / _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|")
print("| |_| | (_| | || (_| | | |_| |  __/ | | |  __/ | | (_| | || (_) | |   ")
print("|____/ \__,_|\__\__,_|  \____|\___|_| |_|\___|_|  \__,_|\__\___/|_|   ")
loop = True
while loop:
    # which file to write
    print("\n")
    print("1. clients")
    print("2. pets")
    print("3. shelters")
    print("4. employees")
    print("5. I want to import data")
    print("6. Exit")
    user_file = input("Which file do you want to create? ")
    while user_file not in ["1", "2", "3", "4", "5", "6"]:
        user_file = input("Please select a valid option: ")
    user_file = int(user_file)

    if user_file == 6:
        exit()

    # how many records to create
    if user_file != 5:
        user_count = input("How many records do you want to generate? ")
        while not user_count.isdigit():
            user_count = input("How many records do you want to generate? ")
        user_count = int(user_count)

    if user_file == 1:
        genClients(user_count)
        print("-> Clients have been generated")
    elif user_file == 2:
        genPets(user_count)
        print("--> Pets have been generated")
    elif user_file == 3:
        if user_count > 1000:
            print("There can't be more than 1,000 shelters")
            user_count = input("How many records do you want to generate? ")
            while not user_count.isdigit():
                user_count = input("How many records do you want to generate? ")
            user_count = int(user_count)
        genShelters(user_count)
        print("---> Shelters have been generated")
    elif user_file == 4:
        genEmployees(user_count)
        print("----> Employees have been generated")
    elif user_file == 5:
        print("Have you generated data for all four tables yet?")
        user_input = input("Y/N ").upper()
        if user_input == "Y":
            print("Are you sure that you have a clients.csv, pets.csv, shelters.csv, and employees.csv?")
            user_input = input("Y/N ").upper()
            if user_input == "Y" and os.path.isfile("clients.csv") and os.path.isfile("pets.csv") and os.path.isfile(
                    "shelters.csv") and os.path.isfile("employees.csv"):
                print("Would you like to import the data into the database tables?")
                user_input = input("Y/N ").upper()
                if user_input == "Y":
                    print("Importing data...")
                    importDatạ()
                    print("Success!")
                    exit()
                else:
                    print("You have chosen to not import data at this time.")
                    exit()
            else:
                print("Files could not be found.")
                exit()
        else:
            print("Please generate data for all four tables.")
            exit()
