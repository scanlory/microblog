#!flask/bin/python
# (c) R. D. Scanlon 2016

r"""
Create SQL Alchemy DB

Runs setup for creating a a lightweight SQLALCHEMY db.
"""


# Imports:
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path


# Program Main function:
def main():
    r"""
    Program entry point.
    :return:
    """

    create_database()


# Function Definitions:
def create_database():
    r"""
    Creates a new SQLALCHEMY db in the main project repository.

    :return:
    """
    db.create_all()
    if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
        api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO,
                            api.version(SQLALCHEMY_MIGRATE_REPO))


# Program state handling:
if __name__ == '__main__':
    main()
