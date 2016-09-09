#!flask/bin/python
# (c) R. D. Scanlon 2016

r"""
Microblog Run

Starts the development web server.
"""


# Imports:
from app import app


# Program Main function:
def main():
    r"""
    Program entry point.
    :return:
    """

    app.run(debug=False)


# Program state handling:
if __name__ == '__main__':
    main()
