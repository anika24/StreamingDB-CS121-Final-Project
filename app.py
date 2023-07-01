"""
Student name(s): Anika Arora, Andy Dimnaku
Student email(s): aarora@caltech.edu, adimnaku@caltech.edu
High-level program overview

******************************************************************************
Python functionality to connect to streamingdb database, where clients and 
admin can view/perform a variety of functions relating to streaming service data
from Netflix, Hulu, Disney+, and Amazon Prime. 
******************************************************************************
"""
import sys  # to print error messages to sys.stderr
import mysql.connector
# To get error codes from the connector, useful for user-friendly
# error-handling
import mysql.connector.errorcode as errorcode

# Debugging flag to print errors when debugging that shouldn't be visible
# to an actual client. ***Set to False when done testing.***
DEBUG = False
IS_ADMIN = False
IS_CLIENT = False

# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='appadmin',
          # Find port in MAMP or MySQL Workbench GUI or with
          # SHOW VARIABLES WHERE variable_name LIKE 'port';
          port='3306',  # this may change!
          password='adminpw',
          database='streamingdb' # replace this with your database name
        )
        print('Successfully connected.\n')
        return conn
    except mysql.connector.Error as err:
        # Remember that this is specific to _database_ users, not
        # application users. So is probably irrelevant to a client in your
        # simulated program. Their user information would be in a users table
        # specific to your database; hence the DEBUG use.
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            # A fine catchall client-facing message.
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
def show_available_services():
    '''
    Displays the services table, which contains basic information about the
    services that are represented in streamingdb. 
    '''
    cursor = conn.cursor()
    sql = 'SELECT service_title, total_users, founding_date FROM services;'
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        print ("{:<15} {:<15} {:<15}".format('service_title','total_users','founding_date'))
        print('-'*45)
        for row in rows:
            (service_title, total_users, founding_date) = row
            print ("{:<15} {:<15} {}".format(service_title, total_users, founding_date))
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')
    show_home()

def show_deals_for_service():
    '''
    Given a service, displays all deals for that given service
    '''
    param1 = input('Enter the service which you would like to look at deals for: ')
    param1 = param1.lower()
    cursor = conn.cursor()
    sql = ''' SELECT deal_title, price, payment_method 
              FROM deals NATURAL JOIN services 
              WHERE service_title = \'%s\';''' % (param1, )
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')
    if not rows:
        print('No deals for this service.')
    else:
        print ("{:<25} {:<20} {:<20}".format('deal_title','price','payment_method'))
        print('-'*65)
        for row in rows:
            (deal_title, price, payment_method) = row
            print ("{:<25} {:<20} {}".format(deal_title, price, payment_method))
    show_home()

def show_average_ratings():
    '''
    Displays the average TV show ratings and average movie ratings for
    each streaming service
    '''
    cursor = conn.cursor()
    sql = ''' SELECT service_title, avg_movie_rating, avg_tv_rating
                FROM 
                    (SELECT service_id, AVG(rating) AS avg_movie_rating
                    FROM contents NATURAL JOIN content_ratings
                    WHERE content_type = 'Movie'
                    GROUP BY service_id) AS movie_avg
                        NATURAL JOIN 
                    (SELECT service_id, AVG(rating) AS avg_tv_rating
                    FROM contents NATURAL JOIN content_ratings
                    WHERE content_type = 'TV show'
                    GROUP BY service_id) AS tv_avg
                        NATURAL JOIN
                    services; '''
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()      
        print ("{:<20} {:<20} {:<20}".format('service_title','avg_movie_rating','avg_tv_rating'))
        print('-'*60) 
        for row in rows:
            (service_title, avg_movie_rating, avg_tv_rating) = row
            print ("{:<20} {:<20} {}".format(service_title, avg_movie_rating, avg_tv_rating))  
        show_home()       
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

def see_service_reviews():
    '''
    Given a service, and rating (integer from 1 - 5), displays all reviews
    for that given service of the rating. 
    '''
    param1 = input('Enter the service which you would like to look at reviews for: ')
    param1 = param1.lower()
    param2 = input('Enter which star reviews you would like to see (integer between 1 - 5) ')
    param2 = int(param2)
    cursor = conn.cursor()
    sql = '''   SELECT service_title, service_rating, review_description
                FROM reviews NATURAL JOIN services
                WHERE service_title = \'%s\' AND service_rating = %d;''' % (param1, param2, )
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')
    if not rows:
        print('No %s star reviews for this service.' % param2)
    else:
        print ("{:<20} {:<20} {:<20}".format('service_title','service_rating','review_description'))
        print('-'*60)
        for row in rows:
            (service_title, service_rating, review_description) = row
            print ("{:<20} {:<20} {}".format(service_title, service_rating, review_description))
    show_home()
    
def find_content():
    '''
    Given a keyword, displays all content that has that keyword in the title. 
    '''
    param1 = input('We can see if our streaming services have specific content. What keyword are you looking for? ')
    cursor = conn.cursor()
    sql = '''   SELECT title, content_type, release_year, on_netflix, on_hulu, on_amazon_prime, on_disney_plus
                FROM contents
                WHERE title LIKE \'%%%s%%\';''' % (param1, )
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')
    if not rows:
        print('There is no content matching the %s keyword.' % param1)   
    else:
        print ("{:<100} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format('title','content_type','release_year', 'on_netflix', 'on_hulu', 'on_amazon_prime', 'on_disney_plus'))
        print('-'*190)
        for row in rows:
            (title, content_type, release_year, on_netflix, on_hulu, on_amazon, on_disney) = row
            print ("{:<100} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format(title, content_type, release_year, on_netflix, on_hulu, on_amazon, on_disney))
    show_home()


def add_rating_to_content_on_service():
    '''
    Admin only privilege
    Given a content title, integer rating between 1 and 10, and service,
    updates the content_ratings table based on our written stored procedure
    and returns the updated tuple.
    '''
    param1 = input('Enter a movie/TV show title which you would like to rate: ')
    param2 = input ('Enter a rating (between 1 and 10): ')
    param2 = float(param2)
    param3 = input('Enter which service the content is on: ')
    param3 = param3.lower()
    cursor = conn.cursor()
    sql = 'CALL update_content_rating(%d, \'%s\', \'%s\');' % (param2, param1, param3, )
    print(sql)
    try:
        cursor.execute(sql)
        sql2 = ''' SELECT title, service_title, rating, num_ratings 
                FROM content_ratings NATURAL JOIN contents NATURAL JOIN services
                WHERE title = \'%s\' AND service_title = \'%s\';''' % (param1, param3, )
        cursor = conn.cursor()
        cursor.execute(sql2)
        rows = cursor.fetchall()
        if not rows:
            print('The input title and service do not have an existing rating in our database.')
        else:
            print('Successfully updated movie rating. Here is the updated row. \n')
            print ("{:<100} {:<15} {:<15} {:<15}".format('title','service_title','rating', 'num_ratings'))
            print('-'*145)
            for row in rows:
                (title, service_title, rating, num_ratings) = row
                print ("{:<100} {:<15} {:<15} {}".format(title, service_title, rating, num_ratings))
            show_home()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')


def add_service_review():
    '''
    Admins can add a review of a service to the services table. Takes in a service name, 
    rating from 1-5, and review comments, and then uses an INSERT statement to update the
    services table. 
    '''
    param1 = input('What service would you like to review? ')
    param2 = input('What is your rating of the service from 1 - 5 (integer value)? ')
    param2 = float(param2)
    param3 = input('Write any comments you have about the service: ')
    cursor = conn.cursor()
    sql1 = 'SELECT service_id FROM services WHERE service_title = \'%s\';' % (param1, )
    try:
        cursor.execute(sql1)
        rows = cursor.fetchall()
        if not rows:
            print('Not a valid streaming service in our database')
        else:
            service_id = rows[0][0]
            sql2 = '''INSERT INTO reviews (service_id, service_rating, review_description) 
                    VALUES (%d, %f, \'%s\');''' % (service_id, param2, param3)
            cursor = conn.cursor()
            cursor.execute(sql2)
            print('Thanks! Your review was successfully added.')
            show_home()
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...') 


# ----------------------------------------------------------------------
# Functions for Logging Users In
# ----------------------------------------------------------------------
# Note: There's a distinction between database users (admin and client)
# and application users (e.g. members registered to a store). You can
# choose how to implement these depending on whether you have app.py or
# app-client.py vs. app-admin.py (in which case you don't need to
# support any prompt functionality to conditionally login to the sql database)

def login():
    '''
    Authenticates a login
    '''
    param1 = input('Enter your usernme: ')
    param2 = input('Enter your password: ')

    cursor = conn.cursor()
    sql = '''SELECT authenticate(\'%s\', \'%s\');''' % (param1, param2, )
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')
    [(val, )] = rows
    if not rows:
        print('Incorrect username or password.\n')
    elif val == 1:
        print('Valid information was entered!\n')
        login_chooser(param1)
    else:
        print('Incorrect username or password.\n')
        show_home()

def login_chooser(username):
    '''
    Chooses either a client or admin role based on the login information
    '''
    cursor = conn.cursor()
    sql = 'SELECT is_admin FROM user_info WHERE username=\'%s\';' % (username, )
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except mysql.connector.Error as err:
        # If you're testing, it's helpful to see more details printed.
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')
    [(val, )] = rows
    global IS_ADMIN
    global IS_CLIENT
    if val == 1:
        IS_ADMIN = True
    else:
        IS_CLIENT = True
    show_home()

def show_home():
    '''
    Displays basic home settings assuming no login yet
    '''
    global IS_ADMIN
    global IS_CLIENT
    if IS_ADMIN:
        show_admin_options()
    elif IS_CLIENT:
        show_client_options()
    else:
        show_options()


# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    print('What would you like to do? ')
    print('  Here are some options of what do: ')
    print('  (s) - Look at the available services')
    print('  (l) - login')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 'l':
        login()
    elif ans == 's':
        print('\n')
        show_available_services()
    else:
        print('Unknown option.')

# Another example of where we allow you to choose to support admin vs. 
# client features  in the same program, or
# separate the two as different app_client.py and app_admin.py programs 
# using the same database.
def show_admin_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    print('\n')
    print('What would you like to do? ')
    print('  Here are some of the changes admins are able to make: ')
    print('  (d) - look at current deals for the streaming services')
    print('  (s) - look at the available streaming services')
    print('  (a) - look at the average movie and TV ratings for each streaming service')
    print('  (r) - look at the reviews for different streaming services')
    print('  (f) - finds content given a keyword')
    print('  (g) - add a rating for a specific content on a streaming service ')
    print('  (ar) - add a review for a streaming service')
    print('  (q) - quit')
    print()
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 's':
        print('\n')
        show_available_services()
    elif ans == 'd':
        print('\n')
        show_deals_for_service()
    elif ans == 'd':
        print('\n')
        show_deals_for_service()
    elif ans == 'a':
        print('\n')
        show_average_ratings()
    elif ans == 'r':
        print('\n')
        see_service_reviews()
    elif ans == 'f':
        print('\n')
        find_content()
    elif ans == 'g':
        print('\n')
        add_rating_to_content_on_service()
    elif ans == 'ar':
        print('\n')
        add_service_review()
    else:
        print('Unknown option.')


def show_client_options():
    """
    Displays options users can choose in the application, such as
    viewing <x>, filtering results with a flag (e.g. -s to sort),
    sending a request to do <x>, etc.
    """
    print('\n')
    print('What would you like to do? ')
    print('  Here are some of the changes clients are able to make: ')
    print('  (d) - look at current deals for the streaming services')
    print('  (s) - look at the available streaming services')
    print('  (a) - look at the average movie and TV ratings for each streaming service')
    print('  (r) - look at the reviews for different streaming services')
    print('  (f) - finds content given a keyword')
    print('  (q) - quit')
    ans = input('Enter an option: ').lower()
    if ans == 'q':
        quit_ui()
    elif ans == 's':
        print('\n')
        show_available_services()
    elif ans == 'd':
        print('\n')
        show_deals_for_service()
    elif ans == 'd':
        print('\n')
        show_deals_for_service()
    elif ans == 'a':
        print('\n')
        show_average_ratings()
    elif ans == 'r':
        print('\n')
        see_service_reviews()
    elif ans == 'f':
        print('\n')
        find_content()
    else:
        print('Unknown option.')

def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    exit()


def main():
    """
    Main function for starting things up.
    """
    show_options()


if __name__ == '__main__':
    # This conn is a global object that other functions can access.
    # You'll need to use cursor = conn.cursor() each time you are
    # about to execute a query with cursor.execute(<sqlquery>)
    conn = get_conn()
    main()
