# -*- coding: utf-8 -*-

__version__ = '0.0.1'

import nltk

try:
    nltk.data.find('tokenizers')
except LookupError:
    nltk.download('popular')
