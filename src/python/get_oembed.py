from subprocess import call
from tempfile import TemporaryFile

def get_oembed( video_token ):
  '''function takes video's token, curls the oembed, and returns the response, and the token'''

  try:
    video_token = int( video_token )
  except:
    print 'video token is wrong... not int'

  token_str = str( video_token )
  response = ''

  with TemporaryFile() as temp:
    call(['curl',('http://vimeo.com/api/oembed.json?url=http%3A//vimeo.com/'+token_str)],stdout=temp)
    temp.seek(0)
    response = temp.read()

  return response, token_str
