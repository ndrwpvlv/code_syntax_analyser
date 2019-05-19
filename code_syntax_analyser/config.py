# -*- coding: utf-8 -*-

from code_syntax_analyser.parsers import PythonParser

# PARSERS
PARSERS = {
    'python': PythonParser,
}
LANGUAGES_ACCEPTED = [key for key in PARSERS]

# GIT
CLONE_PATH_SUFFIX = '/repo/'

# FILES PROCESSING
FILES_NUMBER_LIMIT = 1000

# TEXT PROCESSING
WORDS_TOP_SIZE = 20
WORDS_TYPES_ACCEPTED = ['all', 'verb', 'noun', ]
SYNTAX_TYPES_ACCEPTED = ['all', 'function', 'class', 'variables', ]

# REPORT
REPORTS_TYPES_ACCEPTED = ['all', 'console', 'csv', 'txt', 'json', ]
REPORT_FILENAME = 'report'

TEMPLATE_WORDS_TOP = """
---------------------------------------
TOP WORDS:
---------------------------------------
{% for row in data %}{{ row[0] }} - {{ row[1] }}\n{% endfor %}
"""
