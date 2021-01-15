import models
import app
import getpass
import hashlib
import os


def add_user():
    username = input("Username: ")
    while True:
        user = app.db.session.query(models.User).filter_by(
            username=username).first()
        if user:
            print("That username is already in the database")
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

    salt = os.urandom(32)
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt, 100000)

    user = models.User(username=username,
                       password=hashed_password, salt=salt)
    app.db.session.add(user)
    app.db.session.commit()
    print("User has been added")
    print(app.db.session.query(models.User).all())


def delete_user():
    while True:
        username = input("Enter username: ")
        user = app.db.session.query(models.User).filter_by(
            username=username).first()
        print(user)
        if user:
            confirm = input("Are you sure you want to delete this user? (Y/N)")
            if confirm.lower()[0] == "y":
                app.db.session.delete(user)
                app.db.session.commit()
                break
            else:
                print("Wise choice")
                break
        else:
            print("Could not find a user with that username")
            continue


def prompt():
    print("Options: ")
    print("1- Add user")
    print("2- Delete user")
    print("3- Exit")
    return input("What would you like to do? ")


if __name__ == "__main__":
    print("This program is used to add and delete users from the users table. Use it wisely!")
    while True:
        choice = prompt()
        if not choice.isdigit():
            print("A number, please!")
            continue

        number = int(choice)
        if number == 1:
            add_user()
        elif number == 2:
            delete_user()
        elif number == 3:
            break
        else:
            print("Not a valid option")
    print("Bye-bye!")
