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

CREATE TABLE Adoptions(
    ID INTEGER PRIMARY KEY AUTO_INCREMENT,
    PetID INTEGER,
    ClientID INTEGER,
    Date DATE,
    FOREIGN KEY (PetID) references Pets(PetID),
    FOREIGN KEY (ClientID) references Clients(ClientID)
);

-- in the event of a problem, delete tha tables in the following order
DROP TABLE Fostering, Adoptions;
DROP TABLE ClientToEmployee, EmployeeToShelter, PetToShelter;
DROP TABLE Clients, Employees, Pets, Shelters;



