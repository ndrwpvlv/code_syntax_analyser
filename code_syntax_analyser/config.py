# -*- coding: utf-8 -*-

from code_syntax_analyser.parsers import PythonParser

# PARSERS
PARSERS = {
    'python': PythonParser,
}
LANGUAGES_ACCEPTED = [key for key in PARSERS]

# FILES PROCESSING
FILES_NUMBER_LIMIT = 1000

# TEXT PROCESSING
WORDS_TOP_SIZE = 20
WORDS_TYPES_ACCEPTED = ['ALL', 'VERB', 'NOUN', ]
SYNTAX_TYPES_ACCEPTED = ['ALL', 'FUNCTION', 'CLASS', 'VARIABLE', ]

# REPORT
REPORTS_TYPES_ACCEPTED = ['ALL', 'CONSOLE', 'CSV', 'TXT', 'JSON', ]
REPORT_FILENAME = 'report'

TEMPLATE_WORDS_TOP = """
---------------------------------------
TOP WORDS:
---------------------------------------
{% for row in data %}{{ row[0] }} - {{ row[1] }}\n{% endfor %}
"""
