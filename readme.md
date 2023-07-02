## Final Project: Relational Databases Course

Contributors: Anika Arora and Andy Dimnaku

We created a streaming services databases called streamingdb which contains accumulated data from Netflix, Hulu, Disney+, and Amazon Prime. The data includes information about the content within the streaming services (movies, TV shows, genres, actors, etc.), as well as user reviews about the streaming services and the content they provide. Our data was obtained from four separate Kaggle datasets (one per streaming service), and reviews of the services and content were randomly generated or scraped off the Internet.

Users are able to interact with this application by providing customized queries to searchfor any information regarding streaming services. For example, one can generate all movies on Netflix andHulu released after 2018, which have rating higher than 7.5. Users can also modify the database bysubmitting their own ratings and reviews. Try it out by following the instructions below!

Instructions, once the code has been loaded: 
Go into mysql with --local-infile = 1:
    Example: /usr/local/mysql/bin/mysql --local-infile=1  -u root -p
Once you are in mysql: run the following commands:
    mysql> SET GLOBAL local_infile=1;
    mysql> SET GLOBAL log_bin_trust_function_creators = 1;
    mysql> CREATE DATABASE streamingdb;
    mysql> USE streamingdb;
    mysql> source setup.sql;
    mysql> source load-data.sql;
    mysql> source setup-passwords.sql;
    mysql> source setup-routines.sql;
    mysql> source grant-permissions.sql;
    mysql> source queries.sql;
    mysql> quit;
In the terminal, run:
    python3 app.py

Now, we should be in the python application. 
Press l to login:
To login as an admin: username = netflix1, password = flix123 or 
                      username = disney1, password = google
To login as a client: username = client1, password = IloveCS121
Follow the outputted prompts as you wish. 
Admins have two more options than clients in the database, which involve inserting and updating tuple values. For admin to actually change the database, they have to enter correct inputs to the prompt. To add a review to the streaming service, enter either netflix, hulu, disney+, or amazon prime when prompted which streaming service you would like to review. All other answers will not update anything, since there are no other streaming services in our database. Similarly, to add a rating for a specific content, the content and its corresponding streaming service must exist in our database. A working example is the content title Avatar: The Last Airbender, which is on Netflix. Other combinations of content and streaming service are not guaranteed to exist in our database, and so an update may be invalid. If any of your inputs contain apostrophes, please type two apostrophes to represent one. This is just because of mysql syntax. For example, if you want to add a rating for Grey's Anatomy on Netflix, please input Grey''s Anatomy instead, or otherwise you will get an error. 

We assume that all of the input prompts are inputted with the correct datatypes, and there will be an error otherwise. 
