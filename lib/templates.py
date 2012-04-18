from string import Template
import re

templates_folder = "/home/application/templates/"
javascript_folder = "/home/application/src/javascript/"

def get_template(name):
  path=templates_folder+name
  with open(path) as f:
    return IQTVTemplate(f.read())

def get_javascript(name):
  path=javascript_folder+name
  with open(path) as f:
    return f.read()

class IQTVTemplate(Template):
  pattern = "(?P<escaped>______)|___(?P<named>[_a-z][_a-z0-9]*)|___(?P<braced>[_a-z][_a-z0-9]*)___|(?P<invalid>___)"

  delimiter = "___"
