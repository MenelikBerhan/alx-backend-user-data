#!/usr/bin/env python3
"""Obfuscating log messages using regex substitution.
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Replaces values of `fields` in `message` with `redaction.
    Format of each field value pair: <field>=<value><separator>"""
    pattern = r'({})([^{}]*)'.format("|".join(fields), separator)
    replacement = r'\1={}'.format(redaction)
    return re.sub(pattern, replacement, message)
