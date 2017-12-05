import argparse
import em
import yaml
import os

from kooki.tools.output import Output
from kooki.tools import write_file
from kooki.config import get_kooki_dir

from ..command import Command
from .jar import jar as default_jar

__command__ = 'new'
__description__ = 'Create a new kooki.yaml file'

default_name = 'index'
default_recipe = 'kooki.recipe.web'
default_jars = ['default']
default_template = 'default'

default_content = '''# @document.name

This is a default document generated by *kooki new*.

Enjoy using **kooki**.

*@document.author*
'''

default_metadata = '''document:
    name: Kooki Document
    author: The developpers
'''

class NewCommand(Command):

    def __init__(self):
        super(NewCommand, self).__init__(__command__, __description__)
        self.add_argument('-n', '--name', help='document name')
        self.add_argument('-t', '--template', help='document template')
        self.add_argument('-r', '--recipe', help='document recipe')
        self.add_argument('-j', '--jars', nargs='+', help='documents kooki jars')
        self.add_argument('-m', '--metadata', nargs='+', help='documents metadata sources')
        self.add_argument('-c', '--content', nargs='+', help='documents content sources')

    def callback(self, args):
        self.check_override_config_file()
        self.check_default_jar_available()

        kooki_config_file = {}
        document_info = {}

        self.handle_name(args, document_info)
        self.handle_recipe(args, document_info)
        self.handle_jars(args, document_info)
        self.handle_template(args, document_info)
        self.handle_metadata(args, document_info)
        self.handle_content(args, document_info)

        Output.start_step('kooki.yaml')
        kooki_config_file[document_info['name']] = document_info
        kooki_config_file_yaml = yaml.safe_dump(kooki_config_file)
        write_file('kooki.yaml', kooki_config_file_yaml)
        Output.info(kooki_config_file_yaml[:-1])

    def check_override_config_file(self):
        if os.path.exists('kooki.yaml'):
            response_ok = False
            while not response_ok:
                print('kooki.yaml already exist.')
                response = input("overide it [y/n] (y): ")
                if response == 'n':
                    raise RuntimeError('Existing kooki.yaml has not be changed.')
                elif response == 'y':
                    response_ok = True

    def check_default_jar_available(self):
        default_jar_path = os.path.join(get_kooki_dir(), 'jars', 'default')
        if not os.path.exists(default_jar_path):
            os.makedirs(default_jar_path)
            saved_path = os.getcwd()
            os.chdir(default_jar_path)
            for jar_file, content in default_jar.items():
                write_file(jar_file, content)
            os.chdir(saved_path)

    def handle_name(self, args, document_info):
        Output.start_step('name')
        if args.name:
            document_info['name'] = args.name
        else:
            document_info['name'] = default_name
        Output.info(document_info['name'])

    def handle_recipe(self, args, document_info):
        Output.start_step('recipe')
        if args.recipe:
            document_info['recipe'] = args.recipe
        else:
            document_info['recipe'] = default_recipe
        Output.info(document_info['recipe'])

    def handle_jars(self, args, document_info):
        Output.start_step('jars')
        if args.jars:
            document_info['jars'] = []
            for jar in args.jars:
                document_info['jars'].append(jar)
        else:
            document_info['jars'] = default_jars
        Output.info(yaml.safe_dump(document_info['jars'])[:-1])

    def handle_template(self, args, document_info):
        Output.start_step('template')
        if args.template:
            document_info['template'] = args.template
        else:
            document_info['template'] = default_template
        Output.info(document_info['template'])

    def handle_metadata(self, args, document_info):
        Output.start_step('metadata')
        if args.metadata:
            document_info['metadata'] = []
            for metadata in args.metadata:
                document_info['metadata'].append(metadata)
        else:
            document_info['metadata'] = ['metadata.yaml']
            write_file('metadata.yaml', default_metadata)
        Output.info(yaml.safe_dump(document_info['metadata'])[:-1])

    def handle_content(self, args, document_info):
        Output.start_step('content')
        if args.content:
            document_info['content'] = []
            for content in args.content:
                document_info['content'].append(content)
        else:
            document_info['content'] = ['content.md']
            write_file('content.md', default_content)
        Output.info(yaml.safe_dump(document_info['content'])[:-1])
