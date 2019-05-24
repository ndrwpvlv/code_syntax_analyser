# -*- coding: utf-8 -*-

__version__ = '0.0.2'

import nltk

try:
    nltk.data.find('averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger')

try:
    nltk.data.find('universal_tagset')
except LookupError:
    nltk.download('universal_tagset')
