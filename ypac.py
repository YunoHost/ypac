#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import os
import sys
import shutil

import argh
import jinja2


# CLI Helpers
CLI_COLOR_TEMPLATE = '\033[{:d}m\033[1m'
END_CLI_COLOR = '\033[m'

COLORS_CODES = {
    'red': CLI_COLOR_TEMPLATE.format(31),
    'green': CLI_COLOR_TEMPLATE.format(32),
    'yellow': CLI_COLOR_TEMPLATE.format(33),
    'blue': CLI_COLOR_TEMPLATE.format(34),
    'purple': CLI_COLOR_TEMPLATE.format(35),
    'cyan': CLI_COLOR_TEMPLATE.format(36),
    'white': CLI_COLOR_TEMPLATE.format(37),
}


# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# Prompt helpers


def get_string(question, required=False, from_cli=None):
    if from_cli is not None:
        return from_cli

    answer = raw_input("{cli_start}{question} ? {cli_end}".format(
        cli_start=COLORS_CODES['white'],
        question=question,
        cli_end=END_CLI_COLOR
    ))
    if required and not answer:
        error("{question} is required".format(question=question))
    return answer


def get_boolean(question):
    bool = raw_input("{cli_start}{question} [Yes/No] ? {cli_end}".format(
        cli_start=COLORS_CODES['white'],
        question=question,
        cli_end=END_CLI_COLOR
    ))
    return bool.lower() in ("yes", "y")

# Message helper


def success(message):
    color_print(message, 'green')


def warning(message):
    color_print(message, 'yellow')


def error(message, exit=True):
    color_print(message, 'red')
    if exit:
        sys.exit(1)


def color_print(string, color):
    print("{cli_start}{string}{cli_end}".format(
        cli_start=COLORS_CODES[color],
        string=string,
        cli_end=END_CLI_COLOR
    ))


# Template rendering helper
def render(jinja_env, template, filename, variables):
    rendered_file = jinja_env.get_template(template).render(variables)
    with open(filename, 'wb') as temp_file:
        temp_file.write(rendered_file)


def main(name, id=None, description=None, multi_instance=False, force=False):
    app = dict()

    # Get app settings
    app['name'] = name
    app['id'] = get_string("Application ID (only alpha-numeric character)", from_cli=id).lower()
    app['description'] = get_string("Description", from_cli=description)
    app['multi_instance'] = get_boolean("Multi-instance")

    # Reset output directory
    OUTPUT_PATH = os.path.join(THIS_DIR, '/output/', app['id'])

    if os.path.exists(OUTPUT_PATH):
        if get_boolean("Remove existing {directory} folder".format(directory=OUTPUT_PATH)):
            shutil.rmtree(OUTPUT_PATH)
        else:
            error("{directory} is not empty".format(directory=OUTPUT_PATH))
    os.makedirs(OUTPUT_PATH)

    # Jinja2 environment
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(THIS_DIR + '/templates'),
        trim_blocks=True)

    # Render README template
    render(jinja_env,
           template='README.md.j2',
           filename=os.path.join(OUTPUT_PATH, 'README.md'),
           variables=app
           )

    # Render manifest template
    manifest_vars = app
    manifest_vars['multi_instance'] = "true" if app['multi_instance'] else "false"

    render(jinja_env,
           template='manifest.json.j2',
           filename=os.path.join(OUTPUT_PATH, 'manifest.json'),
           variables=manifest_vars
           )

    # Final message
    success("Package for {name} created in {destination}".format(
        name=app['name'],
        destination=OUTPUT_PATH
    ))


if __name__ == '__main__':
    argh.dispatch_command(main)
