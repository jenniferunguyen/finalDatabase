import mysql.connector, string, re, datetime, tabulate
import csv
from datetime import date
from tabulate import tabulate

db = mysql.connector.connect(
    host="34.94.78.23",
    user="IamRene",
    passwd="40*GermaN",
    database="Final"
)

mycursor = db.cursor()

def customerMenu():
    print("\n")
    print("Welcome to the ")
    print(" __  __        ___         _        _ ")
    print("|  \/  |_  _  | _ \___ _ _| |_ __ _| |")
    print("| |\/| | || | |  _/ _ \ '_|  _/ _` | |")
    print("|_|  |_|\_, | |_| \___/_|  \__\__,_|_|")
    print("        |__/                          ")
    print(">MAIN MENU")
    print("1. My profile")
    print("2. My contact")
    print("3. Sign out")
    user_pick = input("Please select an action: ")
    while user_pick not in ["1", "2", "3"]:
        user_pick = input("Please select a valid option: ")
    print("\n")
    user_pick = int(user_pick)

    if user_pick == 3:
        endApp()
    elif user_pick == 1:
        mycursor.execute("SELECT FirstName, LastName, DateOfBirth, Phone, Email, Address, City, State, Zip, Occupation, Preference, Phase, Status, StatusDate "
                         "FROM Clients "
                         "WHERE ClientID = %s;" % myID)
        thisClient = mycursor.fetchall()
        for c in thisClient:
            thisClient = c
        print("My Profile")
        print("     Name:          " + thisClient[0] + " " + thisClient[1])
        print("     Date of birth: " + (thisClient[2]).strftime("%Y-%m-%d"))
        print("     Phone:         " + thisClient[3])
        print("     Email:         " + thisClient[4])
        print("     Address:       " + thisClient[5] + " " + thisClient[6] + ", " + thisClient[7] + " " + thisClient[8])
        print("     Occupation:    " + thisClient[9])
        print("     Preference:    " + thisClient[10])
        print("     Phase:         " + thisClient[11])
        if thisClient[12] == True:
            status = "APPROVED"
        else:
            status = "PENDING"
        print("     Status:        " + status + " as of " + (thisClient[13]).strftime("%Y-%m-%d"))
        print("Select a field to edit:")
        print("1. Phone")
        print("2. Email")
        print("3. Address")
        print("4. Occupation")
        print("5. Preference")
        print("6. Phase")
        print("7. Delete")
        print("Enter 8 to return to the main menu")
        user_pick = input("Selection: ")
        while user_pick not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            user_pick = input("Please select a valid option: ")
        user_pick = int(user_pick)
        if user_pick == 9:
            customerMenu()
        elif user_pick == 1:
            entry = input("Enter phone number xxx-xxx-xxxx: ")
            # error check phone number format
            phonePattern = "^(\d{3})-(\d{3})-(\d{4})$"
            isPhone = re.match(phonePattern, entry)
            while not isPhone:
                entry = input("Enter valid phone number: ")
                isPhone = re.match(phonePattern, entry)
            mycursor.execute("UPDATE Clients "
                             "SET Phone = %s "
                             "WHERE ClientID = %s;",
                             (entry, myID))
            db.commit()
        elif user_pick == 2:
            entry = input("Enter email: ")
            # error check email format
            emailPattern = "(\w+)@(\w+).(\w+)"
            isEmail = re.match(emailPattern, entry)
            while not isEmail:
                entry = input("Enter valid email: ")
                isEmail = re.match(emailPattern, entry)
            mycursor.execute("UPDATE Clients "
                             "SET Email = %s "
                             "WHERE ClientID = %s;",
                             (entry, myID))
            db.commit()
        elif user_pick == 3:
            entry = [None] * 4
            entry[0] = string.capwords(input("Enter street address: "))
            entry[1] = string.capwords(input("Enter city: "))
            entry[2] = input("Enter state by 2-letter abbreviation: ").upper()
            # error check valid state
            while not entry[2] in ['CA', 'OR', 'WA']:
                entry[2] = input("Please select CA, OR, or WA: ")
            entry[3] = input("Enter zip code: 9")
            # error check valid zip code
            zipPattern = "^\d{4}$"
            isZip = re.match(zipPattern, entry[3])
            while not isZip:
                entry[3] = input("Enter last 4 digits of the zip code: 9")
                isZip = re.match(zipPattern, entry[3])
            entry[3] = "9" + entry[3]
            mycursor.execute("UPDATE Clients "
                             "SET Address = %s, City = %s, State = %s, Zip = %s "
                             "WHERE ClientID = %s;",
                             (entry[0], entry[1], entry[2], entry[3], myID))
            db.commit()
        elif user_pick == 4:
            entry = string.capwords(input("Enter occupation: "))
            mycursor.execute("UPDATE Clients "
                             "SET Occupation = %s "
                             "WHERE ClientID = %s;",
                             (entry, myID))
            db.commit()
        elif user_pick == 5:
            entry = input("Dog or cat: ").lower()
            # error check valid preference
            while entry not in ['dog', 'cat']:
                entry = input("Please select dog or cat: ")
            mycursor.execute("UPDATE Clients "
                             "SET Preference = %s "
                             "WHERE ClientID = %s;",
                             (entry, myID))
            db.commit()
        elif user_pick == 6:
            entry = input("Fostering or adopting: ")
            # error check valid phase
            while entry not in ['fostering', 'adopting']:
                entry = input("Please select fostering or adopting: ")
            mycursor.execute("UPDATE Clients "
                             "SET Phase = %s "
                             "WHERE ClientID = %s;",
                             (entry, myID))
            db.commit()
        elif user_pick == 7:
            user_pick = input("Are you sure you want to delete? Y/N ").upper()
            while user_pick not in ['Y', 'N']:
                user_pick = input("Please select Y/N: ").upper()
            if user_pick == 'Y':
                mycursor.execute("UPDATE Clients "
                                 "SET Deleted = TRUE "
                                 "WHERE ClientID = %s;",
                                 myID)
                db.commit()
                print("You have deleted your account. Please contact Tech Support if you want to retrieve your account.")
                endApp()
            else:
                customerMenu()
    elif user_pick == 2:
        mycursor.execute("SELECT eFirstName, eLastName, ePhone, eEmail "
                         "FROM MyClients "
                         "WHERE ClientID = %s;" % myID)
        thisContact = mycursor.fetchall()
        for c in thisContact:
            thisContact = c
        print("     Name:          " + thisContact[0] + " " + thisContact[1])
        print("     Phone:         " + thisContact[2])
        print("     Email:         " + thisContact[3])
    print("\n")
    customerMenu()

def employeeMenu():
    print("\n")
    print("Welcome to the ")
    print("  ___            _                    ___         _        _ ")
    print(" | __|_ __  _ __| |___ _  _ ___ ___  | _ \___ _ _| |_ __ _| |")
    print(" | _|| '  \| '_ \ / _ \ || / -_) -_) |  _/ _ \ '_|  _/ _` | |")
    print(" |___|_|_|_| .__/_\___/\_, \___\___| |_| \___/_|  \__\__,_|_|")
    print("           |_|         |__/                                  ")
    print(">MAIN MENU")
    print("1. Search")
    print("2. Create new record")
    print("3. Update a record")
    print("4. Add a match")
    print("5. Reports")
    print("6. Sign out")
    user_pick = input("Please select an action: ")
    while user_pick not in ["1", "2", "3","4","5", "6"]:
        user_pick = input("Please select a valid option: ")
    print("\n")
    user_pick = int(user_pick)

    if user_pick == 6:
        endApp()

    if user_pick == 1:
        searchMenu()
    elif user_pick == 2:
        print(">>NEW RECORD")
        print("1. New client record")
        print("2. New pet record")
        user_pick = input("Please select a record type: ")
        while user_pick not in ["1", "2"]:
            user_pick = input("Please select a valid option: ")
        print("\n")
        user_pick = int(user_pick)
        if user_pick == 1:
            addClient()
        else:
            addPet()
    elif user_pick == 3:
        print(">>RECORD UPDATE")
        print("1. Update client record")
        print("2. Update pet record")
        user_pick = input("Please select a record type: ")
        while user_pick not in ["1", "2"]:
            user_pick = input("Please select a valid option: ")
        print("\n")
        user_pick = int(user_pick)
        if user_pick == 1:
            updateClient()
        else:
            updatePet()
    elif user_pick == 4:
        print(">>ADD MATCH")
        print("1. New fostering")
        print("2. New adoption")
        user_pick = input("Please select a record type: ")
        while user_pick not in ["1", "2"]:
            user_pick = input("Please select a valid option: ")
        print("\n")
        user_pick = int(user_pick)
        if user_pick == 1:
            addFostering()
        else:
            addAdoption()
    elif user_pick == 5:
        reportsMenu()
    employeeMenu()

def searchMenu():
    print(">>SEARCH")
    print("1. client by id")
    print("2. pet by id")
    print("3. number of fosters")
    print("4. number of adoptions")
    print("Enter 5 to return to MAIN MENU")
    user_pick = input("Please select an action: ")
    while user_pick not in ["1", "2", "3", "4", "5"]:
        user_pick = input("Please select a valid option: ")
    print("\n")
    user_pick = int(user_pick)

    if user_pick == 5:
        employeeMenu()
    elif user_pick == 1:
        thisID = input("Enter the client id: ")
        try:
            thisID = int(thisID)
        except ValueError:
            print("ERROR: Client id must be numeric")
            print("\n")
            searchMenu()
        print("Client information:")
        mycursor.execute("SELECT FirstName, LastName, DateOfBirth, Phone, Email, Address, City, State, Zip, Occupation, Preference, Phase, Status, StatusDate, Deleted "
                         "FROM Clients "
                         "WHERE ClientID = %s;" % thisID)
        thisClient = mycursor.fetchall()
        for c in thisClient:
            thisClient = c
        print("     Name:          " + thisClient[0] + " " + thisClient[1])
        print("     Date of birth: " + (thisClient[2]).strftime("%Y-%m-%d"))
        print("     Phone:         " + thisClient[3])
        print("     Email:         " + thisClient[4])
        print("     Address:       " + thisClient[5] + " " + thisClient[6] + ", " + thisClient[7] + " " + thisClient[8])
        print("     Occupation:    " + thisClient[9])
        print("     Preference:    " + thisClient[10])
        print("     Phase:         " + thisClient[11])
        if thisClient[12] == True:
            status = "APPROVED"
        else:
            status = "PENDING"
        print("     Status:        " + status + " as of " + (thisClient[13]).strftime("%Y-%m-%d"))
        if thisClient[13] == True:
            condition = "NO"
        else:
            condition = "YES"
        print("     Active:        " + condition)
        if condition == "YES":
            user_pick = input("Get employee contact? Y/N ").upper()
            while user_pick not in ['Y', 'N']:
                user_pick = input("Please select Y/N: ").upper()
            if user_pick == 'Y':
                mycursor.execute("SELECT eFirstName, eLastName, ePhone, eEmail "
                                 "FROM MyClients "
                                 "WHERE ClientID = %s;" % thisID)
                thisContact = mycursor.fetchall()
                for c in thisContact:
                    thisContact = c
                print("     Name:          " + thisContact[0] + " " + thisContact[1])
                print("     Phone:         " + thisContact[2])
                print("     Email:         " + thisContact[3])
    elif user_pick == 2:
        thisID = input("Enter the pet id: ")
        try:
            thisID = int(thisID)
        except ValueError:
            print("ERROR: Client id must be numeric")
            print("\n")
            searchMenu()
        print("Pet information:")
        mycursor.execute("SELECT Name, DateOfBirth, Gender, Type, HealthConcerns, Phase, Deleted "
                         "FROM Pets "
                         "WHERE PetID = %s;" % thisID)
        thisPet = mycursor.fetchall()
        for p in thisPet:
            thisPet = p
        print("     Name:            " + thisPet[0])
        print("     Date of birth:   " + (thisPet[1]).strftime("%Y-%m-%d"))
        print("     Gender:          " + thisPet[2])
        print("     Type:            " + thisPet[3])
        if thisPet[4] == True:
            status = "True"
        else:
            status = "False"
        print("     Health concerns: " + status)
        print("     Phase:           " + thisPet[5])
        if thisPet[6] == True:
            condition = "NO"
        else:
            condition = "YES"
        print("     Active:          " + condition)
        if condition == "YES":
            user_pick = input("Get shelter contact? Y/N ").upper()
            while user_pick not in ['Y', 'N']:
                user_pick = input("Please select Y/N: ").upper()
            if user_pick == 'Y':
                mycursor.execute("SELECT ShelterID, Phone, Email "
                                 "FROM MyPets "
                                 "WHERE PetID = %s;" % thisID)
                thisContact = mycursor.fetchall()
                for c in thisContact:
                    thisContact = c
                print("     Shelter ID:    " + str(thisContact[0]))
                print("     Phone:         " + thisContact[1])
                print("     Email:         " + thisContact[2])
    elif user_pick == 3:
        print("Select filter: ")
        print("1. all fosters")
        print("2. by shelter")
        print("3. by year")
        user_pick = input("Selection: ")
        while user_pick not in ["1", "2", "3"]:
            user_pick = input("Please select a valid option: ")
        user_pick = int(user_pick)
        if user_pick == 1:
            mycursor.execute("SELECT count(ID) "
                             "FROM Fostering;")
            thisCount = mycursor.fetchall()
            for c in thisCount:
                thisCount = c[0]
            print("...There has been " + str(thisCount) + " fosters.")
        elif user_pick == 2:
            mycursor.execute("SELECT S.ShelterID, count(F.ID) "
                             "FROM Fostering F "
                             "JOIN PetToShelter PTS on F.PetID = PTS.PetID "
                             "JOIN Shelters S on S.ShelterID = PTS.ShelterID "
                             "GROUP BY S.ShelterID;")
            thisCount = mycursor.fetchall()
            print(tabulate(thisCount, headers=["ShelterID", "Number of Fosters"]))
        elif user_pick == 3:
            thisYear = input("Enter the year (2000-2021): ")
            # error check for year
            yearPattern = "^\d{4}$"
            isYear = re.match(yearPattern, thisYear)
            if isYear:
                thisYear = int(thisYear)
                if thisYear < 2000:
                    print("Year must be after 2000")
                    isYear = False
                elif thisYear > 2021:
                    print("Year can't be in the future")
                    isYear = False
            while not isYear:
                thisYear = input("Enter valid year: ")
                isYear = re.match(yearPattern, thisYear)
                if isYear:
                    thisYear = int(thisYear)
                    if thisYear < 2000:
                        print("Year must be after 2000")
                        isYear = False
                    elif thisYear > 2021:
                        print("Year can't be in the future")
                        isYear = False
            mycursor.execute("SELECT count(ID) "
                             "FROM Fostering "
                             "WHERE YEAR(StartDate) >= %s and YEAR(StartDate) < %s;",
                             [thisYear, thisYear+1])
            thisCount = mycursor.fetchall()
            for c in thisCount:
                thisCount = c[0]
            print("...There has been " + str(thisCount) + " fosters.")
    elif user_pick == 4:
        print("Select filter: ")
        print("1. all adoptions")
        print("2. by shelter")
        print("3. by year")
        user_pick = input("Selection: ")
        while user_pick not in ["1", "2", "3"]:
            user_pick = input("Please select a valid option: ")
        user_pick = int(user_pick)
        if user_pick == 1:
            mycursor.execute("SELECT count(ID) "
                             "FROM Adoptions;")
            thisCount = mycursor.fetchall()
            for c in thisCount:
                thisCount = c[0]
            print("...There has been " + str(thisCount) + " adoptions.")
        elif user_pick == 2:
            mycursor.execute("SELECT S.ShelterID, count(A.ID) "
                             "FROM Adoptions A "
                             "JOIN PetToShelter PTS on A.PetID = PTS.PetID "
                             "JOIN Shelters S on S.ShelterID = PTS.ShelterID "
                             "GROUP BY S.ShelterID;")
            thisCount = mycursor.fetchall()
            print(tabulate(thisCount, headers=["ShelterID", "Number of Adoptions"]))
        elif user_pick == 3:
            thisYear = input("Enter the year (2000-2021): ")
            # error check for year
            yearPattern = "^\d{4}$"
            isYear = re.match(yearPattern, thisYear)
            if isYear:
                thisYear = int(thisYear)
                if thisYear < 2000:
                    print("Year must be after 2000")
                    isYear = False
                elif thisYear > 2021:
                    print("Year can't be in the future")
                    isYear = False
            while not isYear:
                thisYear = input("Enter valid year: ")
                isYear = re.match(yearPattern, thisYear)
                if isYear:
                    thisYear = int(thisYear)
                    if thisYear < 2000:
                        print("Year must be after 2000")
                        isYear = False
                    elif thisYear > 2021:
                        print("Year can't be in the future")
                        isYear = False
            mycursor.execute("SELECT count(ID) "
                             "FROM Adoptions "
                             "WHERE YEAR(Date) >= %s and YEAR(Date) < %s;",
                             [thisYear, thisYear + 1])
            thisCount = mycursor.fetchall()
            for c in thisCount:
                thisCount = c[0]
            print("...There has been " + str(thisCount) + " adoptions.")
    print("\n")
    searchMenu()

def addClient():
    print("Adding client...")
    entry = [None] * 12
    entry[0] = string.capwords(input("Enter first name: "))
    entry[1] = string.capwords(input("Enter last name: "))
    dob = input("Date of birth YYYY-MM-DD: ")
    # error check date format
    dobPattern = "^(\d{4})-(\d{2})-(\d{2})$"
    isDOB = re.match(dobPattern, dob)
    while not isDOB:
        dob = input("Enter valid date: ")
        isDOB = re.match(dobPattern, dob)
    try:
        entry[2] = datetime.datetime.strptime(dob, '%Y-%m-%d').date()
    except ValueError:
        print("ERROR: Your month or day is out of range. Let's try again")
        print("\n")
        addClient()
    if entry[2] > (datetime.datetime.now() + datetime.timedelta(weeks=-17*52)).date():
        print("ERROR: Client must be at least 17")
        employeeMenu()
    entry[3] = input("Enter phone number xxx-xxx-xxxx: ")
    # error check phone number format
    phonePattern = "^(\d{3})-(\d{3})-(\d{4})$"
    isPhone = re.match(phonePattern, entry[3])
    while not isPhone:
        entry[3] = input("Enter valid phone number: ")
        isPhone = re.match(phonePattern, entry[3])
    entry[4] = input("Enter email: ")
    # error check email format
    emailPattern = "(\w+)@(\w+).(\w+)"
    isEmail = re.match(emailPattern, entry[4])
    while not isEmail:
        entry[4] = input("Enter valid email: ")
        isEmail = re.match(emailPattern, entry[4])
    entry[5] = string.capwords(input("Enter street address: "))
    entry[6] = string.capwords(input("Enter city: "))
    entry[7] = input("Enter state by 2-letter abbreviation: ").upper()
    # error check valid state
    while not entry[7] in ['CA', 'OR', 'WA']:
        entry[7] = input("Please select CA, OR, or WA: ")
    entry[8] = input("Enter zip code: 9")
    # error check valid zip code
    zipPattern = "^\d{4}$"
    isZip = re.match(zipPattern, entry[8])
    while not isZip:
        entry[8] = input("Enter last 4 digits of the zip code: 9")
        isZip = re.match(zipPattern, entry[8])
    entry[8] = "9" + entry[8]
    entry[9] = string.capwords(input("Enter occupation: "))
    entry[10] = input("Dog or cat: ").lower()
    # error check valid preference
    while entry[10] not in ['dog', 'cat']:
        entry[10] = input("Please select dog or cat: ")
    entry[11] = input("Fostering or adopting: ")
    # error check valid phase
    while entry[11] not in ['fostering', 'adopting']:
        entry[11] = input("Please select fostering or adopting: ")
    mycursor.execute("INSERT INTO Clients(FirstName, LastName, DateOfBirth, Phone, Email, "
                     "Address, City, State, Zip,"
                     "Occupation, Preference, Phase,"
                     "Status, StatusDate)"
                     "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",
                     (entry[0], entry[1], entry[2], entry[3], entry[4],
                      entry[5], entry[6], entry[7], entry[8],
                      entry[9], entry[10], entry[11],
                      False, date.today()))
    db.commit()
    mycursor.execute("SELECT MAX(ClientID) "
                     "FROM Clients;")
    myClients = mycursor.fetchall()
    for c in myClients:
        newClient = c[0]
    mycursor.execute("INSERT INTO ClientToEmployee(ClientID, EmployeeID) "
                     "VALUES (%s,%s);",
                     (newClient, myID))
    db.commit()
    print("...")
    print("Successfully added " + entry[0] + " " + entry[1])

def addPet():
    print("Adding pet...")
    entry = [None] * 6
    entry[0] = string.capwords(input("Enter name: "))
    dob = input("Date of birth YYYY-MM-DD: ")
    # error check date format
    dobPattern = "^(\d{4})-(\d{2})-(\d{2})$"
    isDOB = re.match(dobPattern, dob)
    while not isDOB:
        dob = input("Enter valid date: ")
        isDOB = re.match(dobPattern, dob)
    try:
        entry[1] = datetime.datetime.strptime(dob, '%Y-%m-%d').date()
    except ValueError:
        print("ERROR: Your month or day is out of range. Let's try again")
        print("\n")
        addPet()
    if entry[1] >= datetime.datetime.now().date():
        print("ERROR: Pet must have been born")
        employeeMenu()
    entry[2] = input("Male or female: ").lower()
    # error check gender
    while entry[2] not in ['male', 'female']:
        entry[2] = input("Please select male or female: ")
    entry[3] = input("Dog or cat: ").lower()
    # error check type
    while entry[3] not in ['dog', 'cat']:
        entry[3] = input("Please select dog or cat: ")
    entry[4] = input("Does the pet have health concerns? Y/N ").upper()
    # error check health concerns
    while entry[4] not in ['Y', 'N']:
        entry[4] = input("Please select Y/N: ").upper()
    if entry[4] == 'Y':
        entry[4] = False
    else:
        entry[4] = True
    entry[5] = input("Fostering or adopting: ")
    # error check valid phase
    while entry[5] not in ['fostering', 'adopting']:
        entry[5] = input("Please select fostering or adopting: ")
    mycursor.execute("INSERT INTO Pets(Name, DateOfBirth, Gender,"
                     "Type, HealthConcerns, Phase)"
                     "VALUES (%s,%s,%s,%s,%s,%s);",
                     (entry[0], entry[1], entry[2],
                      entry[3], entry[4], entry[5]))
    db.commit()
    mycursor.execute("SELECT MAX(PetID) "
                     "FROM Pets;")
    myPets = mycursor.fetchall()
    for p in myPets:
        newPet = p[0]
    mycursor.execute("SELECT ShelterID "
                     "FROM EmployeeToShelter "
                     "WHERE EmployeeID = %s;" % myID)
    myShelter = mycursor.fetchall()
    for s in myShelter:
        myShelter = s[0]
    mycursor.execute("INSERT INTO PetToShelter(PetID, ShelterID) "
                     "VALUES (%s,%s);",
                     (newPet, myShelter))
    db.commit()
    print("...")
    print("Successfully added " + entry[0])

def updateClient():
    print("Here are your clients: ")
    mycursor.execute("SELECT ClientID, cFirstName, cLastName "
                     "FROM MyClients "
                     "WHERE EmployeeID = %s;" % myID)
    myClients = mycursor.fetchall()
    clientList = []
    for c in myClients:
        clientList.append(c[0])
    print(tabulate(myClients, headers=["ID", "Name"]))
    thisID = input("Enter the id of the client you want to update (or 0 to exit): ")
    try:
        thisID = int(thisID)
    except ValueError:
        print("ERROR: Client id must be numeric")
        print("\n")
        updateClient()
    if thisID == 0:
        employeeMenu()
    if not thisID in clientList:
        print("You do not have access to that client id. Please choose an id from your client list.")
        print("\n")
        updateClient()
    else:
        print("Client information:")
        mycursor.execute("SELECT FirstName, LastName, DateOfBirth, Phone, Email, Address, City, State, Zip, Occupation, Preference, Phase, Status, StatusDate "
                        "FROM Clients "
                        "WHERE ClientID = %s;" % thisID)
        thisClient = mycursor.fetchall()
        for c in thisClient:
            thisClient = c
        print("     Name:          " + thisClient[0] + " " + thisClient[1])
        print("     Date of birth: " + (thisClient[2]).strftime("%Y-%m-%d"))
        print("     Phone:         " + thisClient[3])
        print("     Email:         " + thisClient[4])
        print("     Address:       " + thisClient[5] + " " + thisClient[6] + ", " + thisClient[7] + " " + thisClient[8])
        print("     Occupation:    " + thisClient[9])
        print("     Preference:    " + thisClient[10])
        print("     Phase:         " + thisClient[11])
        if thisClient[12] == True:
            status = "APPROVED"
        else:
            status = "PENDING"
        print("     Status:        " + status + " as of " + (thisClient[13]).strftime("%Y-%m-%d"))
        print("Select a field to edit:")
        print("1. Phone")
        print("2. Email")
        print("3. Address")
        print("4. Occupation")
        print("5. Preference")
        print("6. Phase")
        print("7. Approval status")
        print("8. Delete")
        print("Enter 9 to choose different client")
        user_pick = input("Selection: ")
        while user_pick not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            user_pick = input("Please select a valid option: ")
        user_pick = int(user_pick)
        if user_pick == 9:
            updateClient()
        elif user_pick == 1:
            entry = input("Enter phone number xxx-xxx-xxxx: ")
            # error check phone number format
            phonePattern = "^(\d{3})-(\d{3})-(\d{4})$"
            isPhone = re.match(phonePattern, entry)
            while not isPhone:
                entry = input("Enter valid phone number: ")
                isPhone = re.match(phonePattern, entry)
            mycursor.execute("UPDATE Clients "
                             "SET Phone = %s "
                             "WHERE ClientID = %s;",
                             (entry, thisID))
            db.commit()
        elif user_pick == 2:
            entry = input("Enter email: ")
            # error check email format
            emailPattern = "(\w+)@(\w+).(\w+)"
            isEmail = re.match(emailPattern, entry)
            while not isEmail:
                entry = input("Enter valid email: ")
                isEmail = re.match(emailPattern, entry)
            mycursor.execute("UPDATE Clients "
                             "SET Email = %s "
                             "WHERE ClientID = %s;",
                             (entry, thisID))
            db.commit()
        elif user_pick == 3:
            entry = [None] * 4
            entry[0] = string.capwords(input("Enter street address: "))
            entry[1] = string.capwords(input("Enter city: "))
            entry[2] = input("Enter state by 2-letter abbreviation: ").upper()
            # error check valid state
            while not entry[2] in ['CA', 'OR', 'WA']:
                entry[2] = input("Please select CA, OR, or WA: ")
            entry[3] = input("Enter zip code: 9")
            # error check valid zip code
            zipPattern = "^\d{4}$"
            isZip = re.match(zipPattern, entry[3])
            while not isZip:
                entry[3] = input("Enter last 4 digits of the zip code: 9")
                isZip = re.match(zipPattern, entry[3])
            entry[3] = "9" + entry[3]
            mycursor.execute("UPDATE Clients "
                             "SET Address = %s, City = %s, State = %s, Zip = %s "
                             "WHERE ClientID = %s;",
                             (entry[0], entry[1], entry[2], entry[3], thisID))
            db.commit()
        elif user_pick == 4:
            entry = string.capwords(input("Enter occupation: "))
            mycursor.execute("UPDATE Clients "
                             "SET Occupation = %s "
                             "WHERE ClientID = %s;",
                             (entry, thisID))
            db.commit()
        elif user_pick == 5:
            entry = input("Dog or cat: ").lower()
            # error check valid preference
            while entry not in ['dog', 'cat']:
                entry = input("Please select dog or cat: ")
            mycursor.execute("UPDATE Clients "
                             "SET Preference = %s "
                             "WHERE ClientID = %s;",
                             (entry, thisID))
            db.commit()
        elif user_pick == 6:
            entry = input("Fostering or adopting: ")
            # error check valid phase
            while entry not in ['fostering', 'adopting']:
                entry = input("Please select fostering or adopting: ")
            mycursor.execute("UPDATE Clients "
                             "SET Phase = %s "
                             "WHERE ClientID = %s;",
                             (entry, thisID))
            db.commit()
        elif user_pick == 7:
            entry = input("Approved? T/F ").upper()
            while entry not in ['T', 'F']:
                entry = input("Please select T/F: ").upper()
            if entry == 'F':
                entry = False
            else:
                entry = True
            mycursor.execute("UPDATE Clients "
                             "SET Status = %s, StatusDate = %s "
                             "WHERE ClientID = %s;",
                             (entry, date.today(), thisID))
            db.commit()
        elif user_pick == 8:
            user_pick = input("Are you sure you want to delete? Y/N ").upper()
            while user_pick not in ['Y', 'N']:
                user_pick = input("Please select Y/N: ").upper()
            if user_pick == 'Y':
                mycursor.execute("UPDATE Clients "
                                 "SET Deleted = TRUE "
                                 "WHERE ClientID = %s;",
                                 thisID)
                db.commit()
            else:
                employeeMenu()
        print("...Updated")
        user_pick = input("Update another record? Y/N ").upper()
        while user_pick not in ['Y', 'N']:
            user_pick = input("Please select Y/N: ").upper()
        if user_pick == 'Y':
            updateClient()
        else:
            employeeMenu()

def updatePet():
    print("Here are the pets at your shelter: ")
    mycursor.execute("SELECT PetID, Name, Type, Phase "
                     "FROM MyPets "
                     "WHERE EmployeeID = %s"% myID)
    myPets = mycursor.fetchall()
    petList = []
    for p in myPets:
        petList.append(p[0])
    print(tabulate(myPets, headers=["ID", "Name", "Type", "Phase"]))
    thisID = input("Enter the id of the pet you want to update (or 0 to exit): ")
    try:
        thisID = int(thisID)
    except ValueError:
        print("ERROR: Pet id must be numeric")
        print("\n")
        updatePet()
    if thisID == 0:
        employeeMenu()
    if not thisID in petList:
        print("You do not have access to that pet id. Please choose an id from your shelter's list.")
        print("\n")
        updatePet()
    else:
        print("Pet information:")
        mycursor.execute(
            "SELECT Name, DateOfBirth, Gender, Type, HealthConcerns, Phase "
            "FROM Pets "
            "WHERE PetID = %s;" % thisID)
        thisPet = mycursor.fetchall()
        for p in thisPet:
            thisPet = p
        print("     Name:            " + thisPet[0])
        print("     Date of birth:   " + (thisPet[1]).strftime("%Y-%m-%d"))
        print("     Gender:          " + thisPet[2])
        print("     Type:            " + thisPet[3])
        if thisPet[4] == True:
            status = "True"
        else:
            status = "False"
        print("     Health concerns: " + status)
        print("     Phase:           " + thisPet[5])
        print("Select a field to edit:")
        print("1. Health concerns")
        print("2. Phase")
        print("Enter 3 to choose different pet")
        user_pick = input("Selection: ")
        while user_pick not in ["1", "2", "3"]:
            user_pick = input("Please select a valid option: ")
        user_pick = int(user_pick)
        if user_pick == 3:
            updatePet()
        elif user_pick == 1:
            entry = input("Health conerns? T/F ").upper()
            while entry not in ['T', 'F']:
                entry = input("Please select T/F: ").upper()
            if entry == 'F':
                entry = False
            else:
                entry = True
            mycursor.execute("UPDATE Pets "
                             "SET HealthConcerns = %s "
                             "WHERE PetID = %s;",
                             (entry, thisID))
            db.commit()
        elif user_pick == 2:
            entry = input("Fostering or adopting: ")
            # error check valid phase
            while entry not in ['fostering', 'adopting']:
                entry = input("Please select fostering or adopting: ")
            mycursor.execute("UPDATE Pets "
                             "SET Phase = %s "
                             "WHERE PetID = %s;",
                             (entry, thisID))
            db.commit()
        print("...Updated")
        user_pick = input("Update another record? Y/N ").upper()
        while user_pick not in ['Y', 'N']:
            user_pick = input("Please select Y/N: ").upper()
        if user_pick == 'Y':
            updatePet()
        else:
            employeeMenu()

def addFostering():
    thisID = input("Enter the id of the client: ")
    try:
        thisID = int(thisID)
    except ValueError:
        print("ERROR: Client id must be numeric")
        print("\n")
        addFostering()
    print("Client information:")
    mycursor.execute(
        "SELECT FirstName, LastName, Preference, Phase, Status, StatusDate, Deleted "
        "FROM Clients "
        "WHERE ClientID = %s;" % thisID)
    thisClient = mycursor.fetchall()
    for c in thisClient:
        thisClient = c
    if thisClient[6] == True:
        print("This client is not active.")
        print("\n")
        addFostering()
    if thisClient[3] != "fostering":
        print("This client is looking to adopt.")
        print("\n")
        employeeMenu()
    print("     Name:          " + thisClient[0] + " " + thisClient[1])
    if thisClient[4] == True:
        status = "APPROVED"
    else:
        status = "PENDING"
    print("     Status:        " + status + " as of " + (thisClient[5]).strftime("%Y-%m-%d"))
    if status == "PENDING":
        print("ERROR: Client application is pending. Client must be approved for fostering")
        employeeMenu()
    else:
        print("     Preference:    " + thisClient[2])
        thatID = input("Enter the id of the pet: ")
        try:
            thatID = int(thatID)
        except ValueError:
            print("ERROR: Pet id must be numeric")
            print("\n")
            addFostering()
        mycursor.execute("SELECT Name, Gender, Type, Phase, Deleted "
                         "FROM Pets "
                         "WHERE PetID = %s;" % thatID)
        thisPet = mycursor.fetchall()
        for p in thisPet:
            thisPet = p
        if thisPet[4] == True:
            print("This pet is not active.")
            print("\n")
            addFostering()
        if thisPet[3] != "fostering":
            print("This pet is not up for fostering.")
            print("\n")
            addFostering()
        if thisPet[2] != thisClient[2]:
            print("The client prefers a different pet type.")
            print("\n")
            addFostering()
        print("     Name:          " + thisPet[0])
        print("     Gender:        " + thisPet[1])
        print("     Type:          " + thisPet[2])
    start = input("Enter start date YYYY-MM-DD: ")
    # error check date format
    dobPattern = "^(\d{4})-(\d{2})-(\d{2})$"
    isDOB = re.match(dobPattern, start)
    while not isDOB:
        start = input("Enter valid date: ")
        isDOB = re.match(dobPattern, start)
    try:
        start = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    except ValueError:
        print("ERROR: Your month or day is out of range. Let's try again")
        print("\n")
        addFostering()
    if start < datetime.datetime.now().date():
        print("ERROR: Start date can't be in the past")
        print("\n")
        addFostering()
    mycursor.execute("INSERT INTO Fostering(PetID, ClientID, StartDate, EndDate)"
                     "VALUES (%s,%s,%s,%s);",
                     (thatID, thisID, start, start + datetime.timedelta(days=35)))
    db.commit()
    print("Match complete!")

def addAdoption():
    thisID = input("Enter the id of the client: ")
    try:
        thisID = int(thisID)
    except ValueError:
        print("ERROR: Client id must be numeric")
        print("\n")
        addAdoption()
    print("Client information:")
    mycursor.execute(
        "SELECT FirstName, LastName, Preference, Phase, Status, StatusDate, Deleted "
        "FROM Clients "
        "WHERE ClientID = %s;" % thisID)
    thisClient = mycursor.fetchall()
    for c in thisClient:
        thisClient = c
    if thisClient[6] == True:
        print("This client is not active.")
        print("\n")
        addAdoption()
    if thisClient[3] != "adopting":
        print("This client is looking to foster.")
        print("\n")
        employeeMenu()
    print("     Name:          " + thisClient[0] + " " + thisClient[1])
    if thisClient[4] == True:
        status = "APPROVED"
    else:
        status = "PENDING"
    print("     Status:        " + status + " as of " + (thisClient[5]).strftime("%Y-%m-%d"))
    if status == "PENDING":
        print("ERROR: Client application is pending. Client must be approved for adopting")
        employeeMenu()
    else:
        print("     Preference:    " + thisClient[2])
        thatID = input("Enter the id of the pet: ")
        try:
            thatID = int(thatID)
        except ValueError:
            print("ERROR: Pet id must be numeric")
            print("\n")
            addAdoption()
        mycursor.execute("SELECT Name, Gender, Type, Phase, Deleted "
                         "FROM Pets "
                         "WHERE PetID = %s;" % thatID)
        thisPet = mycursor.fetchall()
        for p in thisPet:
            thisPet = p
        if thisPet[4] == True:
            print("This pet is not active.")
            print("\n")
            addAdoption()
        if thisPet[3] != "adopting":
            print("This pet is not up for adoption.")
            print("\n")
            addAdoption()
        if thisPet[2] != thisClient[2]:
            print("The client prefers a different pet type.")
            print("\n")
            addAdoption()
        print("     Name:          " + thisPet[0])
        print("     Gender:        " + thisPet[1])
        print("     Type:          " + thisPet[2])
    start = input("Enter official transfer date YYYY-MM-DD: ")
    # error check date format
    dobPattern = "^(\d{4})-(\d{2})-(\d{2})$"
    isDOB = re.match(dobPattern, start)
    while not isDOB:
        start = input("Enter valid date: ")
        isDOB = re.match(dobPattern, start)
    try:
        start = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    except ValueError:
        print("ERROR: Your month or day is out of range. Let's try again")
        print("\n")
        addAdoption()
    if start < datetime.datetime.now().date():
        print("ERROR: Date can't be in the past")
        print("\n")
        addAdoption()
    mycursor.execute("INSERT INTO Adoptions(PetID, ClientID, Date)"
                     "VALUES (%s,%s,%s);",
                     (thatID, thisID, start))
    db.commit()
    mycursor.execute("UPDATE Pets SET Deleted = TRUE WHERE PetID = %s" % thatID)
    db.commit()
    mycursor.execute("UPDATE PetToShelter SET Deleted = TRUE WHERE PetID = %s" % thatID)
    db.commit()
    print("Match complete!")

def reportsMenu():
    print(">>REPORTS")
    print("1. Pets by shelter")
    print("2. Pending fostering applications")
    print("3. Pending adoption applications")
    print("4. Approved fostering applications (never fostered before)")
    print("5. Approved adoption applications (never adopted before)")
    print("Enter 6 to return to MAIN MENU")
    user_pick = input("Please select an action: ")
    while user_pick not in ["1", "2", "3", "4", "5", "6"]:
        user_pick = input("Please select a valid option: ")
    print("\n")
    user_pick = int(user_pick)

    if user_pick == 6:
        employeeMenu()
    elif user_pick == 1:
        myShelter = input("Enter shelter ID: ")
        while myShelter not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            myShelter = input("Please select a valid shelter: ")
        print("\n")
        myShelter = int(myShelter)
        print("View option: ")
        print("1. all pets")
        print("2. all cats")
        print("3. all dogs")
        user_pick = input("Please select an option: ")
        while user_pick not in ["1", "2", "3"]:
            user_pick = input("Please select a valid option: ")
        print("\n")
        user_pick = int(user_pick)
        if user_pick == 1:
            mycursor.execute("SELECT DISTINCT PetID, Name, DateOfBirth, Type, HealthConcerns, Phase "
                             "FROM MyPets "
                             "WHERE ShelterID = %s" % myShelter)
            mySearch = mycursor.fetchall()
            myHeaders = ["ID", "Name", "DateOfBirth", "Type", "HealthConcerns", "Phase"]
            print(tabulate(mySearch, headers=myHeaders))
        elif user_pick == 2:
            mycursor.execute("SELECT DISTINCT PetID, Name, DateOfBirth, HealthConcerns, Phase "
                             "FROM MyPets "
                             "WHERE Type = 'cat' and ShelterID = %s" % myShelter)
            mySearch = mycursor.fetchall()
            myHeaders = ["ID", "Name", "DateOfBirth", "HealthConcerns", "Phase"]
            print(tabulate(mySearch, headers=myHeaders))
        else:
            mycursor.execute("SELECT DISTINCT PetID, Name, DateOfBirth, HealthConcerns, Phase "
                             "FROM MyPets "
                             "WHERE Type = 'dog' and ShelterID = %s" % myShelter)
            mySearch = mycursor.fetchall()
            myHeaders = ["ID", "Name", "DateOfBirth", "HealthConcerns", "Phase"]
            print(tabulate(mySearch, headers=myHeaders))

    elif user_pick == 2 or user_pick == 3:
        if user_pick == 2:
            myPhase = 'fostering'
        else:
            myPhase = 'adopting'
        mycursor.execute("SELECT ClientID, FirstName, LastName, DateOfBirth, Phone, Email, "
                         "Address, City, State, Zip, Occupation, Preference, StatusDate "
                         "FROM Clients "
                         "WHERE Phase = %s and Status = 0 and Deleted = 0 "
                         "ORDER BY StatusDate;", [myPhase])
        mySearch = mycursor.fetchall()
        myHeaders = ["ID", "FirstName", "LastName", "DateOfBirth", "Phone", "Email",
                     "Address", "City", "State", "Zip", "Occupation", "Preference", "StatusDate"]
        print(tabulate(mySearch, headers=myHeaders))

    elif user_pick == 4:
        mycursor.execute("SELECT C.ClientID, C.FirstName, C.LastName, C.DateOfBirth, C.Phone, C.Email, "
                         "C.Address, C.City, C.State, C.Zip, C.Occupation, C.Preference, C.StatusDate "
                         "FROM Clients C "
                         "LEFT JOIN Fostering F on C.ClientID = F.ClientID "
                         "WHERE F.ClientID is null and C.Phase = 'fostering' and C.Status = 1 and C.Deleted = 0 "
                         "ORDER BY StatusDate;")
        mySearch = mycursor.fetchall()
        myHeaders = ["ID", "FirstName", "LastName", "DateOfBirth", "Phone", "Email",
                     "Address", "City", "State", "Zip", "Occupation", "Preference", "StatusDate"]
        print(tabulate(mySearch, headers=myHeaders))
    elif user_pick == 4:
        mycursor.execute("SELECT C.ClientID, C.FirstName, C.LastName, C.DateOfBirth, C.Phone, C.Email, "
                         "C.Address, C.City, C.State, C.Zip, C.Occupation, C.Preference, C.StatusDate "
                         "FROM Clients C "
                         "LEFT JOIN Adoptions A on C.ClientID = A.ClientID "
                         "WHERE A.ClientID is null and C.Phase = 'adopting' and C.Status = 1 and C.Deleted = 0 "
                         "ORDER BY StatusDate;")
        mySearch = mycursor.fetchall()
        myHeaders = ["ID", "FirstName", "LastName", "DateOfBirth", "Phone", "Email",
                     "Address", "City", "State", "Zip", "Occupation", "Preference", "StatusDate"]
        print(tabulate(mySearch, headers=myHeaders))

    # export as csv option
    user_pick = input("Export search as csv? Y/N ").upper()
    while user_pick not in ['Y', 'N']:
        user_pick = input("Please select Y/N: ").upper()
    if user_pick == 'Y':
        fileName = input("Enter a file name (excluding .csv): ")
        # error check file name
        filePattern = ".*\.csv$"
        isFile = re.match(filePattern, fileName)
        while isFile or fileName[-1] == ".":
            fileName = input("Enter valid file name: ")
            isFile = re.match(filePattern, fileName)
        fileName = "./" + fileName + ".csv"
        print(fileName)
        csv_file = open(fileName, "w", newline='')
        writer = csv.writer(csv_file)
        writer.writerow(myHeaders)
        for x in mySearch:
            writer.writerow(x)
    else:
        employeeMenu()

def endApp():
    print("\n")
    print("Thank you for visiting. Have a great day!")
    print("     |\_/|                  ")
    print("     | @ @   See you! ")
    print("     |   <>              _  ")
    print("     |  _/\------____ ((| |))")
    print("     |               `--' |   ")
    print(" ____|_       ___|   |___.' ")
    print("/_/_____/____/_______|")
    exit()

print("\n")
print("Welcome to the")
print(" ____      _     ____  _          _ _              ____        _        _                     ")
print("|  _ \ ___| |_  / ___|| |__   ___| | |_ ___ _ __  |  _ \  __ _| |_ __ _| |__   __ _ ___  ___  ")
print("| |_) / _ \ __| \___ \| '_ \ / _ \ | __/ _ \ '__| | | | |/ _` | __/ _` | '_ \ / _` / __|/ _ \ ")
print("|  __/  __/ |_   ___) | | | |  __/ | ||  __/ |    | |_| | (_| | || (_| | |_) | (_| \__ \  __/ ")
print("|_|   \___|\__| |____/|_| |_|\___|_|\__\___|_|    |____/ \__,_|\__\__,_|_.__/ \__,_|___/\___|")
print("\n")

loop = True
loginNum = 0
while loop:
    print("Please select your use type: ")
    print("1. Client")
    print("2. Employee")
    print("3. Exit")
    user_pick = input("Selection: ")
    while user_pick not in ["1", "2", "3"]:
        user_pick = input("Please select a valid option: ")
    user_pick = int(user_pick)

    if user_pick == 3:
        endApp()

    if user_pick == 1:
        myID = input('Enter your client id: ')
        while not myID.isdigit():
            print("ERROR: Your id must be numeric")
            myID = input('Enter your client id: ')
        myID = int(myID)
        mycursor.execute("SELECT MAX(ClientID) "
                         "FROM Clients;")
        totalClients = mycursor.fetchall()
        for t in totalClients:
            totalClients = t[0]
        if myID > totalClients:
            print("Invalid id.")
            break
        user_name = input("Username: ")
        user_pass = input("Password: ")
        if user_name != user_pass:
            print("         Invalid log-in.")
            loginNum += 1
            print("         Remaining tries: " + str(3 - loginNum))
            if loginNum == 3:
                print("         Please contact Tech Support.")
                exit()
            print("\n")
        else:
            customerMenu()
    elif user_pick == 2:
        myID = input('Enter your employee id: ')
        while not myID.isdigit():
            print("ERROR: Your id must be numeric")
            myID = input('Enter your employee id: ')
        myID = int(myID)
        mycursor.execute("SELECT MAX(EmployeeID) "
                         "FROM Employees;")
        totalEmployees = mycursor.fetchall()
        for t in totalEmployees:
            totalEmployees = t[0]
        if myID > totalEmployees:
            print("Invalid id.")
            break
        user_name = input("Username: ")
        user_pass = input("Password: ")
        if user_name != user_pass:
            print("         Invalid log-in.")
            loginNum += 1
            print("         Remaining tries: " + str(3-loginNum))
            if loginNum == 3:
                print("         Please contact Tech Support.")
                exit()
            print("\n")
        else:
            employeeMenu()


