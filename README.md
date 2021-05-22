# Pet Shelter Database

Jennifer Nguyen
CPSC 408

# Instructions
## Setup
1. use createTables.sql to generate the tables
2. run dataGenerator.py to generate and import data into tables
## Application
3. use main.py to open the commandline application
4. to experience the full functionality of the app, please choose the employee use type 
(Hint: enter the exact same thing for both the username and password to access the database)

# Known Errors
none

# Project Requirements
Assuming at Employee Level,
1. Print/display records with "5. Reports"
2. Query for data with various parameters with "1. Search"
3. Create a new record with "2. Create a new record"
4. Delete records with either "3. Update a record" or "4 Add a match >> 2. New adoption"
5. Update records with "3. Update a record"
6. Commit & rollback can be found in dataGenerator.py
7. Generate reports that can be exported with "5. Reports"
8. The query to count fosters by shelters uses a group-by clause
9. Sub-queries are used in logGenerator.py to find eligible matches between client and pets
10. Both views involve joins across at least 3 tables
11. Referential integrality is checked throughout
12. Database views and indexes can be found created in createTables.sql