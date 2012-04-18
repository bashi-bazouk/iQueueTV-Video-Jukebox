from subprocess import call, Popen
from tempfile import TemporaryFile
from PyOpenGraph import PyOpenGraph
import json

def get_oembed(token):
  url='http://vimeo.com/api/oembed.json?url=http%3A//vimeo.com/'+str(token)
  response = ''

  with TemporaryFile() as temp:
    call(['curl',url],stdout=temp)
    temp.seek(0)
    return json.loads(temp.read())

def get_og_data(token):
  return (PyOpenGraph('http://vimeo.com/'+str(token))).metadata


