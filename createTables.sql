-- information tables
CREATE TABLE Clients(
    ClientID INTEGER PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(30),
    LastName VARCHAR(30),
    DateOfBirth DATE,
    Phone VARCHAR(12),
    Email VARCHAR(50),
    Address VARCHAR(50),
    City VARCHAR(30),
    State VARCHAR(2),
    Zip VARCHAR(5),
    Occupation VARCHAR(100),
    Preference VARCHAR(3),
    Phase VARCHAR(10),
    Status BOOLEAN,
    StatusDate DATE,
    Deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE Pets(
    PetID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(30),
    DateOfBirth DATE,
    Gender VARCHAR(10),
    Type VARCHAR(3),
    HealthConcerns BOOLEAN,
    Phase VARCHAR(10),
    Deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE Shelters(
    ShelterID INTEGER PRIMARY KEY AUTO_INCREMENT,
    Phone VARCHAR(12),
    Email VARCHAR(50),
    Address VARCHAR(50),
    City VARCHAR(30),
    State VARCHAR(2),
    Zip VARCHAR(5),
    Deleted BOOLEAN DEFAULT FALSE
);

CREATE TABLE Employees(
    EmployeeID INTEGER PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(30),
    LastName VARCHAR(30),
    DateOfBirth DATE,
    Phone VARCHAR(12),
    Email VARCHAR(50),
    Address VARCHAR(50),
    City VARCHAR(30),
    State VARCHAR(2),
    Zip VARCHAR(5),
    Deleted BOOLEAN DEFAULT FALSE
);

-- connection tables
CREATE TABLE ClientToEmployee(
    ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    ClientID INTEGER,
    EmployeeID INTEGER,
    Deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (ClientID) references Clients(ClientID),
    FOREIGN KEY (EmployeeID) references Employees(EmployeeID)
);

CREATE TABLE PetToShelter(
    ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    PetID INTEGER,
    ShelterID INTEGER,
    Deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (PetID) references Pets(PetID),
    FOREIGN KEY (ShelterID) references Shelters(ShelterID)
);

CREATE TABLE EmployeeToShelter(
    ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    EmployeeID INTEGER,
    ShelterID INTEGER,
    Deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (EmployeeID) references Employees(EmployeeID),
    FOREIGN KEY (ShelterID) references Shelters(ShelterID)
);

CREATE TABLE Fostering(
    ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    PetID INTEGER,
    ClientID INTEGER,
    StartDate DATE,
    EndDate DATE,
    FOREIGN KEY (PetID) references Pets(PetID),
    FOREIGN KEY (ClientID) references Clients(ClientID)
);

-- logging tabels
CREATE TABLE Adoptions(
    ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    PetID INTEGER,
    ClientID INTEGER,
    Date DATE,
    FOREIGN KEY (PetID) references Pets(PetID),
    FOREIGN KEY (ClientID) references Clients(ClientID)
);

-- indexes
CREATE UNIQUE INDEX idx_client
ON Clients(clientID);

CREATE UNIQUE INDEX idx_pet
ON Pets(petID);

CREATE UNIQUE INDEX idx_employee
ON Employees(EmployeeID);

-- database views
CREATE VIEW MyClients AS
SELECT C.ClientID,C.FirstName cFirstName,C.LastName cLastName,C.DateOfBirth,
       C.Phone cPhone,C.Email cEmail,C.Address,C.City,C.State,C.Zip,
       C.Occupation,C.Preference,C.Phase,C.Status,C.StatusDate,
       E.EmployeeID, E.FirstName eFirstName, E.LastName eLastName, E.Email eEmail, E.Phone ePhone
FROM Clients C
JOIN ClientToEmployee CTE ON C.ClientID = CTE.ClientID
JOIN Employees E ON E.EmployeeID = CTE.EmployeeID
WHERE C.Deleted = 0;

CREATE VIEW MyPets AS
SELECT S.ShelterID, S.Phone, S.Email, P.PetID, P.Name, P.Phase, P.DateOfBirth, P.Type, P.HealthConcerns, E.EmployeeID
FROM Shelters S
JOIN PetToShelter PTS ON S.ShelterID = PTS.ShelterID
JOIN Pets P on P.PetID = PTS.PetID
JOIN EmployeeToShelter ETS on PTS.ShelterID = ETS.ShelterID
JOIN Employees E on E.EmployeeID = ETS.EmployeeID
WHERE P.Deleted = 0;

-- in the event of a problem, delete tha tables in the following order
-- DROP VIEW MyClients, MyPets;
-- DROP TABLE Fostering, Adoptions;
-- DROP TABLE ClientToEmployee, EmployeeToShelter, PetToShelter;
-- DROP TABLE Clients, Employees, Pets, Shelters;


