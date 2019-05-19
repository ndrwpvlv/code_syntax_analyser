# code_syntax_analyser

**code_syntax_analyser** - second homework of OTUS Python course. Run script to get unique verbs, nouns or all together from code 

## Installation
Download source or clone repository and execute:
```
pip3 install git+https://github.com/ndrwpvlv/code_syntax_analyser.git
```
If you have some permissions errors try this one:
```
sudo -H pip3 install git+https://github.com/ndrwpvlv/code_syntax_analyser.git

```

## Basic usage
Console usage of package
```
usage: python3 -m code_syntax_analyser [-h] [-g GIT_URL] [-p PATH]
                            [-f FILES_NUMBER_LIMIT] [-l LANGUAGE]
                            [-e EXTENSIONS] [-t WORDS_TOP_SIZE]
                            [-y WORDS_TYPE] [-s SYNTAX_TYPE] [-r REPORT_TYPE]
                            [-c]

It make counting of words in functions, classes and variables names

optional arguments:

  -h, --help                 show this help message and exit
  -g, --git_url              URL of Git repository (enter with http:// or https://)
  -p, --path                 Directory path for code analysis
  -f, --files_number_limit   Limit of files number for analysis, default is 1000
  -l, --language             Code language. Default is 'python'. Java support is in
                             development.
  -e, --extensions           Files extensions. Default is all files. Example enter .py
  -t, --words_top_size       Maximum number of top useful words. Default is 20
  -y, --words_type           Type of words: 'verb' - verbs, 'noun' - nouns, 'all' - all
  -s, --syntax_type          Type of syntax: 'class' - classes, 'function' -
                             functions, 'variable' - variables, 'a' - all
  -r, --report_type          Type of report: 'json', 'csv', 'txt', 'console'
  -c, --cleanup              Use temporary directory and cleanup it. 
                             Use it when you need to cleanup temp directory after words processing 
```

Example with downloading git, processing nouns from classes and delete downloaded repo: 
```
python3 -m code_syntax_analyser -g https://github.com/ndrwpvlv/code_syntax_analyser -p /home/ -e py -y noun -s class -c

```

## Requirements
```
gitdb2==2.0.5
GitPython==2.1.11
Jinja2==2.10.1
MarkupSafe==1.1.1
nltk==3.4.1
six==1.12.0
smmap2==2.0.5
```

## Contributors
Andrei S. Pavlov (https://github.com/ndrwpvlv/)
