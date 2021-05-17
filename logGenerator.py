import mysql.connector
import datetime

def run():
    db = mysql.connector.connect(
        host="34.94.78.23",
        user="IamRene",
        passwd="40*GermaN",
        database="Final"
    )

    mycursor = db.cursor()

    print("Generating history for Fostering...")

    # select eligible pets for fostering
    mycursor.execute("SELECT PetID "
                     "FROM Pets "
                     "WHERE DateOfBirth <= '2009-01-01' AND Phase = 'fostering'; ")
    myPets = mycursor.fetchall()

    # select eligible clients for fostering
    mycursor.execute("SELECT ClientID "
                     "FROM Clients  "
                     "WHERE Phase = 'fostering' AND Status = 1 AND StatusDate <= '2009-06-01';")
    myClients = mycursor.fetchall()

    # create all possible matches based on dates
    mycursor.execute("SELECT P.PetID, C.ClientID, C.StatusDate "
                     "FROM (SELECT PetID, DateOfBirth, Type, Phase "
                     "FROM Pets WHERE DateOfBirth <= '2009-01-01' AND Phase = 'fostering') P "
                     "LEFT JOIN (SELECT ClientID, Preference, Phase, StatusDate "
                     "FROM Clients WHERE Phase = 'fostering' AND Status = 1 AND StatusDate <= '2009-06-01') C "
                     "ON P.DateOfBirth > C.StatusDate AND P.Type = C.Preference AND P.Phase = C.Phase;")
    myPairings = mycursor.fetchall()

    # filter actual matches based on first-come, first-served
    usedPets = []
    usedClients = [None]
    matchesF = []
    for pair in myPairings:
        if (not (pair[0] in usedPets)) and (not (pair[1] in usedClients)):
            usedPets.append(pair[0])
            usedClients.append(pair[1])
            matchesF.append(pair)

    # insert into table
    for m in matchesF:
        mycursor.execute("INSERT INTO Fostering(PetID, ClientID, StartDate, EndDate)"
                         "VALUES (%s,%s,%s,%s);",
                         (m[0], m[1], m[2] + datetime.timedelta(days=14), m[2] + datetime.timedelta(days=35)))
        db.commit()

    # change phase of fostered animals to adopting
    for m in matchesF:
        mycursor.execute("UPDATE Pets SET Phase = 'adopting' WHERE PetID = %s" % (m[0]))
        db.commit()

    print("Generating history for Adoptions...")

    # select eligible pets for adoptions
    mycursor.execute("SELECT PetID "
                     "FROM Pets "
                     "WHERE DateOfBirth <= '2016-01-01' AND Phase = 'adopting'; ")
    myPets = mycursor.fetchall()

    # select eligible clients for adoptions
    mycursor.execute("SELECT ClientID "
                     "FROM Clients  "
                     "WHERE Phase = 'adopting' AND Status = 1 AND StatusDate <= '2016-06-01';")
    myClients = mycursor.fetchall()

    # create all possible matches based on dates
    mycursor.execute("SELECT P.PetID, C.ClientID, C.StatusDate "
                     "FROM (SELECT PetID, DateOfBirth, Type, Phase "
                     "FROM Pets WHERE DateOfBirth <= '2016-01-01' AND Phase = 'adopting') P "
                     "LEFT JOIN (SELECT ClientID, Preference, Phase, StatusDate "
                     "FROM Clients WHERE Phase = 'adopting' AND Status = 1 AND StatusDate <= '2016-06-01') C "
                     "ON P.DateOfBirth > C.StatusDate AND P.Type = C.Preference AND P.Phase = C.Phase;")
    myPairings = mycursor.fetchall()

    # filter actual matches based on first-come, first-served
    usedPets = []
    usedClients = [None]
    matchesA = []
    for pair in myPairings:
        if (not (pair[0] in usedPets)) and (not (pair[1] in usedClients)):
            usedPets.append(pair[0])
            usedClients.append(pair[1])
            matchesA.append(pair)

    # insert into table
    for m in matchesA:
        mycursor.execute("INSERT INTO Adoptions(PetID, ClientID, Date)"
                         "VALUES (%s,%s,%s);",
                         (m[0], m[1], m[2] + datetime.timedelta(days=3)))
        db.commit()

    # soft delete adopted pets
    for m in matchesA:
        mycursor.execute("UPDATE Pets SET Deleted = TRUE WHERE PetID = %s" % (m[0]))
        db.commit()
        mycursor.execute("UPDATE PetToShelter SET Deleted = TRUE WHERE PetID = %s" % (m[0]))
        db.commit()

    print("Success!")



