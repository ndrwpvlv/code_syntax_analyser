# -*- coding: utf-8 -*-

import collections

import nltk

from .helpers import flat_list, str_split_camelcase, str_split_snakecase, Filters, list_values_to_str


class TextTokenizer(Filters):
    """
    Basic class with ntlk tokenizing of words list
    """

    def __init__(self, words_list: list):
        """
        :param words_list: List of words
        """
        super(TextTokenizer, self).__init__()
        self.names = list_values_to_str(words_list)
        self.words = [n.lower() for n in self.names_split()]
        self.tokens = self.words_tokenizer()
        self.filter_add('all', self.words_get)
        self.filter_add('verb', self.verbs_get)
        self.filter_add('noun', self.nouns_get)

    def words_tokenizer(self) -> list:
        return nltk.pos_tag(self.words)

    def names_split(self) -> list:
        return flat_list(
            [str_split_snakecase(n) for n in flat_list([str_split_camelcase(name) for name in self.names])])

    def words_get(self):
        return self.words

    def tokens_get(self):
        return self.tokens

    def verbs_get(self):
        return [token[0] for token in self.tokens if len(self.tokens) > 0 and token[1][0] is 'V']

    def nouns_get(self):
        return [token[0] for token in self.tokens if len(self.tokens) > 0 and token[1][0] is 'N']


class WordsStatistic(Filters):
    """
    Basic class for making words count statistics
    """

    def __init__(self, words: list):
        """
        :param words: List of words, list
        """
        super(WordsStatistic, self).__init__()
        self.words = list_values_to_str(words)
        self.filter_add('top', self.words_top_get)
        self.filter_add('top_dict', self.words_top_to_dict)

    def words_top_get(self, words_list_size: int) -> list:
        return [[word, count] for word, count in collections.Counter(self.words).most_common(words_list_size)]

    def words_top_to_dict(self, words_list_size: int) -> dict:
        return {row[0]: row[1] for row in self.words_top_get(words_list_size)}
