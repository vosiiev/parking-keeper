# parking-keeper

This program was developed for a real parking management, therefore GUI has Ukrainian localisation. There are still some features to be added, however the main logic has already been developed.

Parking lists every customer it has and gives them unique numbers (plastic cards in real life). Every client has his/her fullname, phone number and list of cars he/she owns. The system a journal (table) with info about every parking event. A user (shift supervisor) needs to create a customer's row in a table if it doesn't exist yet and then create an event based on customer's data.

It is required for user to log in and open the shift before using the system. There are 2 types of users: admin and shift supervisor. The first one has extended access to the database: he can edit or delete rows in tables.
