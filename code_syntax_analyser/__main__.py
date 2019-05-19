# -*- coding: utf-8 -*-

import argparse
import errno
import os
import sys

from code_syntax_analyser.config import *
from code_syntax_analyser.helpers import git_clone, url_check, extensions_format, directory_cleanup, path_format, \
    directory_temp_create, directory_check_exist_and_permissions
from code_syntax_analyser.parsers import CodeSource
from code_syntax_analyser.reports import Report
from code_syntax_analyser.texts import TextTokenizer, WordsStatistic


def args_get() -> dict:
    parser = argparse.ArgumentParser(prog='code_syntax_analyser',
                                     description='Counting of words in functions, classes and variables names', )
    parser.add_argument('-g', '--git_url', default='https://github.com/ndrwpvlv/code_analyser',
                        help="URL of Git repository", type=str)
    parser.add_argument('-p', '--path', default=os.getcwd(), help="Directory path for code analysis", type=str)
    parser.add_argument('-f', '--files_number_limit', default=FILES_NUMBER_LIMIT,
                        help="Limit of files number for analysis, default is {}".format(FILES_NUMBER_LIMIT), type=int)
    parser.add_argument('-l', '--language', default='python',
                        help="Code language. Default is python. Java support is in development.", type=str)
    parser.add_argument('-e', '--extensions', default='.py',
                        help="Files extensions. Default is all files. Example enter .py", type=str)
    parser.add_argument('-t', '--words_top_size', default=WORDS_TOP_SIZE,
                        help="Maximum number of top useful words. Default is {}".format(WORDS_TOP_SIZE), type=int)
    parser.add_argument('-y', '--words_type', default='all',
                        help="Type of words: 'verb' - verbs, 'noun' - nouns, 'all' - all", type=str)
    parser.add_argument('-s', '--syntax_type', default='all',
                        help="Type of syntax: 'class' - classes, 'function' - functions, 'variable' - variables, "
                             "'a' - all", type=str)
    parser.add_argument('-r', '--report_type', default='all',
                        help="Type of report: 'json', 'csv', 'txt', 'console', 'all'", type=str)
    parser.add_argument('-c', '--cleanup', action='store_true', help='Use temporary directory and cleanup it',
                        default=False)

    args = parser.parse_args(sys.argv[1:])

    return {
        'git_url': url_check(args.git_url),
        'path': path_format(args.path) if directory_check_exist_and_permissions(args.path) else sys.exit(errno.EACCES),
        'files_number_limit': args.files_number_limit if args.files_number_limit > 0 else FILES_NUMBER_LIMIT,
        'language': args.language if args.language in LANGUAGES_ACCEPTED else LANGUAGES_ACCEPTED[0],
        'extensions': extensions_format(args.extensions),
        'words_top_size': args.words_top_size if args.words_top_size > 0 else WORDS_TOP_SIZE,
        'words_type': args.words_type if args.words_type in WORDS_TYPES_ACCEPTED else WORDS_TYPES_ACCEPTED[0],
        'syntax_type': args.syntax_type if args.syntax_type in SYNTAX_TYPES_ACCEPTED else SYNTAX_TYPES_ACCEPTED[0],
        'report_type': args.report_type if args.report_type in REPORTS_TYPES_ACCEPTED else REPORTS_TYPES_ACCEPTED[0],
        'cleanup': args.cleanup,
    }


def parser_set(*args, **kwargs) -> object:
    return kwargs['parsers'][kwargs['language']](*args)


def main():
    args = args_get()
    print('-----------------\nCODE_SYNTAX_ANALYSER\n-----------------\n')
    print('Solution variables:')
    for key in args:
        print('{}: {}'.format(key, args[key]))
    print('-----------------\n')

    try:
        path_temp = directory_temp_create(args['path'])
    except OSError:
        sys.exit('ERROR :: Access denied. Error - {}'.format(errno.EACCES))

    repo_path = git_clone(args['git_url'], path_temp)
    code_source = CodeSource(repo_path, args['extensions'], args['files_number_limit'])
    parser = parser_set(code_source.paths, parsers=PARSERS, language=args['language'])

    tokenizer = TextTokenizer(parser.filter_by(args['syntax_type']))
    words_statistic = WordsStatistic(tokenizer.filter_by(args['words_type']))
    words_top = words_statistic.filter_by('top', args['words_top_size'])
    report = Report(words_top, REPORT_FILENAME, TEMPLATE_WORDS_TOP, args['path'])
    report.filter_by(args['report_type'])
    print('-----------------\nPROCESSING IS FINISHED')
    if args['cleanup']:
        directory_cleanup(path_temp)
        os.rmdir(path_temp)
        print('-----------------\nDIRECTORY IS CLEANED')


if __name__ == '__main__':
    main()
