# -*- coding: utf-8 -*-

import ast

from .helpers import flatten_list, get_files_paths, format_path, filter_tokens_by


class CodeSource:
    """
    Class for processing sources paths
    """

    def __init__(self, path: str, files_extensions: list, files_number_limit: int, ):
        """
        :param path: Path or parent source code directory, str
        :param files_extensions: List of files extensions, list
        :param files_number_limit: Number of files to process, int
        """
        self.path = format_path(path)
        self.files_extensions = files_extensions
        self.files_number_limit = files_number_limit
        self.paths = get_files_paths(self.path, self.files_extensions, self.files_number_limit)


class CodeParser:
    """
    Parent class of all parsers
    """

    def __init__(self, paths: list, allowed_keys: list, ):
        """
        :param paths: List of path for files processing, list
        :param allowed_keys: List of allowed abstract types, list
        """
        self.paths = paths
        self.allowed_keys = allowed_keys
        self.tokens = []

    def filter_names_by(self, key):
        return filter_tokens_by(self.tokens, key, self.allowed_keys)


class PythonParser(CodeParser):
    """
    Parser of Python syntax with AST
    """

    def __init__(self, paths: list, allowed_keys: list, ):
        """
        :param paths: List of file paths for processing, list
        """
        super(PythonParser, self).__init__(paths, allowed_keys, )
        self.trees = self.parse_files()
        self.tokens = self.tokens_extract()

    @staticmethod
    def parse_file(path: str) -> any:
        """
        Get syntax tree with ast
        :param path: Path of file, str
        :return:
        """
        with open(path, 'r', encoding='utf-8') as file_handler:
            file_content = file_handler.read()
        try:
            return ast.parse(file_content)
        except SyntaxError as e:
            print(e)
            return None

    def parse_files(self) -> list:
        """
        Processing multiple files which stored in self.paths
        :return: list of ast trees
        """
        return [self.parse_file(path) for path in self.paths if self.parse_file(path)]

    def tokens_extract(self) -> list:
        """
        Extract tokens from multiple trees
        :return: List of names with tokens
        """
        return flatten_list(
            [[self.extract_node_name(node) for node in ast.walk(tree) if self.extract_node_name(node)] for
             tree in self.trees if tree])

    @staticmethod
    def extract_node_name(node: ast) -> list:
        """
        Extract name from ast-node
        :param node: AST node
        :return: list with [name, token]
        """
        if any([isinstance(node, ast.FunctionDef), isinstance(node, ast.AsyncFunctionDef)]) and not all(
                [node.name.startswith('__'), node.name.endswith('__')]):
            return [node.name, 'FUNCTION']
        elif isinstance(node, ast.ClassDef):
            return [node.name, 'CLASS']
        elif isinstance(node, ast.Name) and not all([node.id.startswith('__'), node.id.endswith('__')]):
            return [node.id, 'VARIABLE']
        elif isinstance(node, ast.Attribute):
            return [node.attr, 'VARIABLE']


class JavaParser(CodeParser):
    """
    Parser of Java syntax
    """

    def __init__(self, paths: list, allowed_keys: list, ):
        super(JavaParser, self).__init__(paths, allowed_keys, )
