import mysql.connector, string, re, datetime, tabulate
from datetime import date
from tabulate import tabulate

db = mysql.connector.connect(
    host="34.94.78.23",
    user="IamRene",
    passwd="40*GermaN",
    database="Final"
)

mycursor = db.cursor()

def employeeMenu():
    print("\n")
    print("Welcome to the ")
    print("  ___            _                    ___         _        _ ")
    print(" | __|_ __  _ __| |___ _  _ ___ ___  | _ \___ _ _| |_ __ _| |")
    print(" | _|| '  \| '_ \ / _ \ || / -_) -_) |  _/ _ \ '_|  _/ _` | |")
    print(" |___|_|_|_| .__/_\___/\_, \___\___| |_| \___/_|  \__\__,_|_|")
    print("           |_|         |__/                                  ")
    print(">MAIN MENU")
    print("1. View records")
    print("2. Create new record")
    print("3. Update a record")
    print("4. Add a match")
    print("5. Sign out")
    user_pick = input("Please select an action: ")
    while user_pick not in ["1", "2", "3","4","5"]:
        user_pick = input("Please select a valid option: ")
    print("\n")
    user_pick = int(user_pick)

    if user_pick == 5:
        endApp()

    if user_pick == 1:
        print(">>VIEW")
        # TODO display records; query for data; generate reports; query with group-by
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
            addAdoptions()
        # TODO soft delete, rollback
    employeeMenu()

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
    mycursor.execute("SELECT C.ClientID, C.FirstName, C.LastName "
                     "FROM Clients C "
                     "JOIN ClientToEmployee CTE ON C.ClientID = CTE.ClientID "
                     "JOIN Employees E ON E.EmployeeID = CTE.EmployeeID "
                     "WHERE C.Deleted = 0 and E.EmployeeID = %s;" % myID)
    myClients = mycursor.fetchall()
    clientList = []
    for c in myClients:
        clientList.append(c[0])
    print(tabulate(myClients, headers=["ID", "Name"]))
    thisID = input("Enter the id of the client you want to update: ")
    try:
        thisID = int(thisID)
    except ValueError:
        print("ERROR: Client id must be numeric")
        print("\n")
        updateClient()
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
        while user_pick not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
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
                                 (thisID))
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
    mycursor.execute("SELECT P.PetID, P.Name, P.Type, P.Phase "
                     "FROM Pets P "
                     "JOIN PetToShelter PTS on P.PetID = PTS.PetID "
                     "JOIN EmployeeToShelter ETS on PTS.ShelterID = ETS.ShelterID "
                     "JOIN Employees E on E.EmployeeID = ETS.EmployeeID "
                     "WHERE P.Deleted = 0 and E.EmployeeID = %s"% myID)
    myPets = mycursor.fetchall()
    petList = []
    for p in myPets:
        petList.append(p[0])
    print(tabulate(myPets, headers=["ID", "Name", "Type", "Phase"]))
    thisID = input("Enter the id of the pet you want to update: ")
    try:
        thisID = int(thisID)
    except ValueError:
        print("ERROR: Client id must be numeric")
        print("\n")
        updateClient()
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
            status = "YES"
        else:
            status = "NONE"
        print("     Health concerns: " + status)
        print("     Phase:           " + thisPet[5])
        print("Select a field to edit:")
        print("1. Health concerns")
        print("2. Phase")
        print("Enter 3 to choose different client")
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
        break
    elif user_pick == 2:
        myID = input('Enter your employee id: ')
        while not myID.isdigit():
            print("ERROR: Your id must be numeric")
            myID = input('Enter your employee id: ')
        myID = int(myID)
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


