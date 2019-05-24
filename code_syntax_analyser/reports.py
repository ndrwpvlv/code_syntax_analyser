# -*- coding: utf-8 -*-

import json

from jinja2 import Template

from .helpers import Filters, format_path


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
        self.path = format_path(path)
        self.add_filter('CONSOLE', self.console_log)
        self.add_filter('JSON', self.write_json)
        self.add_filter('CSV', self.write_csv)
        self.add_filter('TXT', self.write_txt)
        self.add_filter('ALL', self.gen_reports)

    def console_log(self):
        template = Template(self.template)
        print(template.render(data=self.data))

    def write_txt(self):
        template = Template(self.template)
        with open('{}{}.txt'.format(self.path, self.filename), 'w') as fw:
            fw.write(template.render(data=self.data))

    def write_json(self):
        with open('{}{}.json'.format(self.path, self.filename), 'w') as fw:
            fw.write(json.dumps(self.data))

    def write_csv(self):
        with open('{}{}.csv'.format(self.path, self.filename), 'w') as fw:
            fw.writelines('{}\n'.format(','.join(map(str, line))) for line in self.data)

    def gen_reports(self):
        """Generate all reports"""
        for report in self.filters:
            if self.filters[report].__name__ is not self.gen_reports.__name__:
                self.filters[report]()
