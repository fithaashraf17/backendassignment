

# imports
import argparse


from src.models import Base, engine, session, User


parser = argparse.ArgumentParser(description="MyCart cli App")

# Add the arguments
parser.add_argument('-m', '--migrate', type=str, help='create the database tables')
parser.add_argument('-u', '--username', type=str, help='Username for the new user')
parser.add_argument('-p', '--password', type=str, help='password for the new user')
parser.add_argument('-n', '--name', type=str, help='Name for the new user')
parser.add_argument('-e', '--email', type=str, help='Email for the new user')


# Execute the parse_args() method
args = parser.parse_args()


def migrate():
    """
    A migrate command for creating database tables
   
    """
    Base.metadata.create_all(engine)
    print("Database created successfully")


def add_user():
    """
    create new user in db
    
    """
    username = args.username
    password = args.password
    name = args.name
    email = args.email

    if username and password and name and email:

        user = User(username=username, password=password, name=name, email=email)
        session.add(user)
        session.commit()
        print("User added successfully")


if __name__ == '__main__':
    if args.migrate:
        migrate()

    if args.username:
        add_user()
