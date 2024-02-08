#!/usr/bin/env python3
"""Obfuscating log messages using regex substitution.
"""
from typing import List
import logging
import re


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
