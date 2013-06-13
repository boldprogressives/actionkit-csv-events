DJANGO_DEBUG = "1"
DJANGO_DEBUG_TOOLBAR = "1" 

SITE_NAME = "My Organization"

SECRET_KEY = "secret!"

ACTIONKIT_DATABASE_NAME = "ak_yourclientdbname"
ACTIONKIT_DATABASE_USER = "username"
ACTIONKIT_DATABASE_PASSWORD = "password"

ACTIONKIT_API_HOST = "act.example.com"
ACTIONKIT_API_USER = "api_username"
ACTIONKIT_API_PASSWORD = "api_password"

if __name__ == '__main__':

    import random, sys, os

    assert not os.path.exists(sys.argv[1]), "Please enter a path to a file that doesn't already exist"

    vars = {}

    vars['DJANGO_SECRET'] = ''.join([random.choice('abcdefghijklmnopqrxtuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-=_+') for i in range(30)])

    vars['SITE_NAME'] = raw_input("What is your organization's name? ")
    vars['ACTIONKIT_API_HOST'] = raw_input("Enter the base URL of your Actionkit instance (e.g. https://act.example.com) ")
    vars['ACTIONKIT_API_USER'] = raw_input("Enter the username of an Actionkit user with API access: ")
    vars['ACTIONKIT_API_PASSWORD'] = raw_input("What is the password for that user? ")
    vars['ACTIONKIT_DATABASE_NAME'] = raw_input("What is your Actionkit database name? (e.g. ak_example) ")
    vars['ACTIONKIT_DATABASE_USER'] = raw_input("Enter a username that you use to connect to the Actionkit client-db: ")
    vars['ACTIONKIT_DATABASE_PASSWORD'] = raw_input("What is the password for that database user? ")
        
    env = " ".join(["=".join((key, val)) for key, val in vars.items()])

    with open(sys.argv[1], 'w') as fp:
        print >> fp, env
