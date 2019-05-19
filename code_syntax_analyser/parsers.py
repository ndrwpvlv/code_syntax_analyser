# -*- coding: utf-8 -*-

import ast

from .helpers import flat_list, Filters, files_paths_get, path_format


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
        self.path = path_format(path)
        self.files_extensions = files_extensions
        self.files_number_limit = files_number_limit
        self.paths = files_paths_get(self.path, self.files_extensions, self.files_number_limit)


class CodeParser(Filters):
    """
    Parent class of all parsers. Based on Filters cls. Have basic functions to get syntax names from extracted with Child parsers tokens.
    """

    def __init__(self, paths: list, ):
        """
        :param paths: List of file paths for processing, list
        """
        super(CodeParser, self).__init__()
        self.paths = paths
        self.tokens = []

        self.filter_add('all', self.names_get)
        self.filter_add('function', self.functions_get)
        self.filter_add('class', self.classes_get)
        self.filter_add('variable', self.variables_get)

    def functions_get(self) -> list:
        """Get functions by tokens from self.tokens"""
        return [f[0] for f in list(filter(lambda x: x[1] == 'F', self.tokens))]

    def classes_get(self) -> list:
        """Get classes by tokens from self.tokens"""
        return [c[0] for c in list(filter(lambda x: x[1] == 'C', self.tokens))]

    def variables_get(self) -> list:
        """Get variables by tokens from self.tokens"""
        return [v[0] for v in list(filter(lambda x: x[1] == 'V', self.tokens))]

    def names_get(self) -> list:
        return [token[0] for token in self.tokens]


class PythonParser(CodeParser):
    """
    Parser of Python syntax with ast
    """

    def __init__(self, paths: list, ):
        """
        :param paths: List of file paths for processing, list
        """
        super(PythonParser, self).__init__(paths, )
        self.trees = self.files_syntax_parse()
        self.tokens = self.tokens_extract()

    @staticmethod
    def file_syntax_parse(path: str) -> any:
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

    def files_syntax_parse(self) -> list:
        """
        Processing multiple files which stored in self.paths
        :return: list of ast trees
        """
        return [self.file_syntax_parse(path) for path in self.paths if self.file_syntax_parse(path)]

    def tokens_extract(self) -> list:
        """
        Extract tokens from multiple trees
        :return: List of names with tokens
        """
        return flat_list(
            [[self.name_extract_from_node(node) for node in ast.walk(tree) if self.name_extract_from_node(node)] for
             tree in self.trees if tree])

    @staticmethod
    def name_extract_from_node(node: ast) -> list:
        """
        Extract name from ast-node
        :param node: AST node
        :return: list with [name, token]
        """
        if (isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef)) and not (
                node.name.startswith('__') and node.name.endswith('__')):
            return [node.name, 'F']
        elif isinstance(node, ast.ClassDef):
            return [node.name, 'C']
        elif isinstance(node, ast.Name) and not (
                node.id.startswith('__') and node.id.endswith('__')):
            return [node.id, 'V']
        elif isinstance(node, ast.Attribute):
            return [node.attr, 'V']


class JavaParser(CodeParser):
    """
    Parser of Java syntax
    """

    def __init__(self, paths: list, ):
        super(JavaParser, self).__init__(paths, )
