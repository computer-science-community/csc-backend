"""
This program is used to manage the users in the users table.
Only CSC officers should be able to run this file on the server
"""

import models
import app
import getpass
import hashlib
import os


def add_user():
    """
    Asks for a username and password to add a new user
    """
    while True:
        username = input("Username: ")
        user = app.db.session.query(models.User).filter_by(
            username=username).first()
        if user:
            print("That username is already in the database.")
            continue
        else:
            break

    while True:
        password = getpass.getpass("Password: ")
        confirm_password = getpass.getpass("Confirm Password: ")
        if password == confirm_password:
            break
        else:
            print("Passwords don't match. Try again")

    # Hash the password and store the username, hash, and salt
    salt = os.urandom(32)
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt, 100000)
    user = models.User(username=username,
                       password=hashed_password, salt=salt)
    app.db.session.add(user)
    app.db.session.commit()
    print("User has been added.")


def show_users():
    """
    Displays all the users in the database
    """
    users = app.db.session.query(models.User).all()
    if not users:
        print("No users in the database")
    else:
        print("Users:")
        for user in users:
            print(user)


def delete_user():
    """
    Delete one user from the database
    """
    while True:
        username = input("Enter username to delete: ")
        user = app.db.session.query(models.User).filter_by(
            username=username).first()
        if user:
            confirm = input(
                "Are you sure you want to delete this user? (Y/N) ")
            if confirm.lower()[0] == "y":
                app.db.session.delete(user)
                app.db.session.commit()
                print("User deleted.")
                break
            else:
                print("Wise choice.")
                break
        else:
            print("Could not find a user with that username.")
            continue


def login():
    """
    Make the user log in before granting access
    """
    users = app.db.session.query(models.User).all()
    if not users:
        print("You're the first one here! Add a user for yourself")
        add_user()

    print("Please log in")
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    user = app.db.session.query(models.User).filter_by(
        username=username).first()

    if not user:
        return False
    else:
        stored_password = user.password
        salt = user.salt

    new_key = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt, 100000)
    if stored_password == new_key:
        return True
    else:
        return False


def prompt():
    print("\nOptions: ")
    print("1- Add user")
    print("2- Show users")
    print("3- Delete user")
    print("4- Exit")
    return input("What would you like to do? ")


if __name__ == "__main__":
    while not login():
        print("Incorrect Credentials")
        pass

    print("This program is used to manage the admin user table. Use it wisely!")

    while True:
        choice = prompt()
        if not choice.isdigit():
            print("A number, please!")
            continue

        number = int(choice)
        if number == 1:
            add_user()
        elif number == 2:
            show_users()
        elif number == 3:
            delete_user()
        elif number == 4:
            break
        else:
            print("Not a valid option")
    print("Bye-bye!")
