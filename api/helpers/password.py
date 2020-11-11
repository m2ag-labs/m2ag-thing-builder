import os
import htpasswd


# https://github.com/thesharp/htpasswd

class Password:
    @staticmethod
    def change_password(data):
        with htpasswd.Basic(os.getenv('HOME') + "/.m2ag-labs/.htpasswd") as userdb:
            try:
                userdb.change_password(data['user'], data['password'])
            except htpasswd.basic.UserNotExists:
                return False
        return True

    @staticmethod
    def add_user(data):
        with htpasswd.Basic(os.getenv('HOME') + "/.m2ag-labs/.htpasswd") as userdb:
            try:
                userdb.add(data['user'], data['password'])
            except htpasswd.basic.UserExists:
                return False
        return True

    @staticmethod
    def delete_user(data):
        with htpasswd.Basic(os.getenv('HOME') + "/.m2ag-labs/.htpasswd") as userdb:
            try:
                userdb.pop(data['user'])
            except htpasswd.basic.UserNotExists:
                return False
        return True

    @staticmethod
    def get_users():
        with htpasswd.Basic(os.getenv('HOME') + "/.m2ag-labs/.htpasswd") as userdb:
            try:
                return userdb.users
            except Exception:
                return False
