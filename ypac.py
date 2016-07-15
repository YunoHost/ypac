#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import os
import sys
import shutil

import jinja2

# CLI Helpers
CLI_COLOR_TEMPLATE = '\033[{:d}m\033[1m'
END_CLI_COLOR = '\033[m'

colors_codes = {
    'red'   : CLI_COLOR_TEMPLATE.format(31),
    'green' : CLI_COLOR_TEMPLATE.format(32),
    'yellow': CLI_COLOR_TEMPLATE.format(33),
    'blue'  : CLI_COLOR_TEMPLATE.format(34),
    'purple': CLI_COLOR_TEMPLATE.format(35),
    'cyan'  : CLI_COLOR_TEMPLATE.format(36),
    'white' : CLI_COLOR_TEMPLATE.format(37),
}


# Capture our current directory
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# Main variable
app = dict()

# Prompt helpers
def get_string(question, required = False):
    answer = raw_input("{cli_start}{question} ? {cli_end}".format(
                cli_start=colors_codes['white'],
                question=question,
                cli_end=END_CLI_COLOR
            ))
    if required and not answer:
        error("{question} is required".format(question=question))
    return answer

def get_boolean(question):
    bool = raw_input("{cli_start}{question} [Yes/No] ? {cli_end}".format(
                cli_start=colors_codes['white'],
                question=question,
                cli_end=END_CLI_COLOR
            ))
    return bool.lower() in ("yes", "y")

# Message helper
def warning(message):
    color_print(message, 'yellow')

def error(message, exit = True):
    color_print(message, 'red')
    if exit:
        sys.exit(1)

def color_print(string, color):
    print("{cli_start}{string}{cli_end}".format(
            cli_start=colors_codes[color],
            string=string,
            cli_end=END_CLI_COLOR
        ))


# Template rendering helper
def render(template, filename, variables):
    rendered_file = jinja_env.get_template(template).render(variables)
    with open(os.path.join(OUTPUT_PATH, filename), 'wb') as temp_file:
        temp_file.write(rendered_file)


if __name__ == '__main__':

    # Get app settings
    app['name'] = get_string("Application name", required = True)
    app['id'] = get_string("Application ID (only alpha-numeric character)").lower()
    app['description'] = get_string("Description")
    app['multi_instance'] = get_boolean("Multi-instance")

    # Reset output directory
    OUTPUT_PATH = THIS_DIR + '/output/' + app['id']
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
    render('README.md.j2', 'README.md', app)

    # Render manifest template
    manifest_vars = app
    manifest_vars['multi_instance'] = "true" if app['multi_instance'] else "false" 
    render('manifest.json.j2', 'manifest.json', manifest_vars)
