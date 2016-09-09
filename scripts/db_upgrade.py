#!flask/bin/python
# (c) R. D. Scanlon 2016

r"""
SQL Alchemy DB Upgrade

Copies and re-versions the current application db to a newer version.
"""


# Imports:
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO


# Program Main function:
def main():
    r"""
    Program entry point.
    :return:
    """

    upgrade_db()


# Functions/Classes/etc.:
def upgrade_db():
    """
    Upgrade the current SQLALCHEMY Database 1 version.

    :return:
    """
    api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
    print('Current database version:', str(v))


# Program state handling:
if __name__ == '__main__':
    main()
