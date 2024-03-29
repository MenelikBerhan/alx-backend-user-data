#!/usr/bin/env python3
"""Obfuscating log messages using regex substitution.
"""
from typing import List
import logging
import mysql.connector
import re
import os

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Replaces values of `fields` in `message` with `redaction`.
    Format of each field value pair: <field>=<value><separator>"""
    pattern = r'({})([^{}]*)'.format("|".join(fields), separator)
    replacement = r'\1={}'.format(redaction)
    return re.sub(pattern, replacement, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"       # replacement for self.fields' values
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"         # separator b/n each <field>=<value> pairs

    def __init__(self, fields: List[str]):
        """Initialize formatter with list of fields to redact."""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields    # fields whose values are to be redacted

    def format(self, record: logging.LogRecord) -> str:
        """After redacting `fields` in the `record`'s message,
        formats the specified record as text."""
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR
            )
        return super().format(record)


def get_logger() -> logging.Logger:
    """Creates and returns a `Logger` instance."""
    # create a logger called `user_data` with `INFO` log level
    # logger = logging.Logger('user_data', logging.INFO)
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False    # prevent propagation of msgs to other loggers

    # create a stream handler and set log level & formatter
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)

    # add stream handler to logger and return
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connection to a mysql database. Database name,
    user name, password and host are read from environment variables."""
    mysql_connection = mysql.connector.connection.MySQLConnection(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )
    return mysql_connection


def main():
    """Retrieves all rows in the `users` table and,
    after redacting, displays each row."""
    # get db connection
    connection = get_db()
    if connection and connection.is_connected():
        with connection.cursor() as cursor:
            result = cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
            logger = get_logger()
            for row in rows:
                # set fileds in `<filed>=<value>;` format
                msg = f"name={row[0]};email={row[1]};phone={row[2]};" +\
                    f"ssn={row[3]};password={row[4]};ip={row[5]};" +\
                    f"last_login={row[6]};user_agent={row[7]};"
                logger.info(msg)

        connection.close()

    else:
        print("Could not connect to db.")


if __name__ == '__main__':
    main()
