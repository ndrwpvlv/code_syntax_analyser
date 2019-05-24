# -*- coding: utf-8 -*-

import collections

import nltk

from .helpers import flatten_list, str_split_camelcase, str_split_snakecase, Filters, list_values_to_str, \
    filter_tokens_by


class TextTokenizer:
    """
    Basic class with ntlk tokenizing of words list
    """

    def __init__(self, words_list: list, allowed_keys: list, ):
        """
        :param words_list: List of words
        """
        self.names = list_values_to_str(words_list)
        self.allowed_keys = [k.upper() for k in allowed_keys]
        self.words = [n.lower() for n in self.split_names()]
        self.tokens = self.words_tokenizer(self.words)

    def split_names(self) -> list:
        return flatten_list(
            [str_split_snakecase(n) for n in flatten_list([str_split_camelcase(name) for name in self.names])])

    @staticmethod
    def words_tokenizer(words: list) -> list:
        return nltk.pos_tag(words, tagset='universal')

    def tokens_get(self):
        return self.tokens

    def filter_words_by(self, key: str) -> list:
        return filter_tokens_by(self.tokens, key, self.allowed_keys)


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
        self.add_filter('top', self.words_top_get)
        self.add_filter('top_dict', self.words_top_to_dict)

    def words_top_get(self, words_list_size: int) -> list:
        return [[word, count] for word, count in collections.Counter(self.words).most_common(words_list_size)]

    def words_top_to_dict(self, words_list_size: int) -> dict:
        return {row[0]: row[1] for row in self.words_top_get(words_list_size)}
