import subprocess
from sys import exc_info
from tempfile import TemporaryFile

def check( token ):
  curl_results = ''
  with TemporaryFile() as temp:
    subprocess.call(['curl','-IL',('http://www.vimeo.com/'+str(token))],stdout=temp)
    temp.seek(0)
    curl_results = temp.read()

  curl_result_lines = curl_results.split('\n')
  good_link = False
  if 'HTTP/1.0 404 Not Found\r' in curl_result_lines:
    pass
  else:
    good_link = True

  return good_link
