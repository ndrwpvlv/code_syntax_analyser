# -*- coding: utf-8 -*-

import json
import os

from jinja2 import Template

from .helpers import Filters, path_format


class Report(Filters):
    """
    Basic class of reports generator
    """

    def __init__(self, data: list, filename: str, template_jinja: str, path: str, ):
        """

        :param data: List of data for report processing, list
        :param filename: Filename for saving files, str
        :param template_jinja: Jinja2 template in string, str
        :param path of saving files, str
        """
        super(Report, self).__init__()
        self.data = data
        self.filename = filename
        self.template = template_jinja
        self.path = path_format(path)
        self.filter_add('console', self.console_log)
        self.filter_add('json', self.json_write)
        self.filter_add('csv', self.csv_write)
        self.filter_add('txt', self.txt_write)
        self.filter_add('all', self.reports_gen_all)

    def console_log(self):
        template = Template(self.template)
        print(template.render(data=self.data))

    def txt_write(self):
        template = Template(self.template)
        with open('{}{}.txt'.format(self.path, self.filename), 'w') as fw:
            fw.write(template.render(data=self.data))

    def json_write(self):
        with open('{}{}.json'.format(self.path, self.filename), 'w') as fw:
            fw.write(json.dumps(self.data))

    def csv_write(self):
        with open('{}{}.csv'.format(self.path, self.filename), 'w') as fw:
            fw.writelines('{}\n'.format(','.join(map(str, line))) for line in self.data)

    def reports_gen_all(self):
        """Generate all reports"""
        for report in self.filters:
            if self.filters[report].__name__ is not self.reports_gen_all.__name__:
                self.filters[report]()
