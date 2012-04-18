import zmq
import json
from uuid import uuid4
from mongrel2 import handler
import subprocess
from tempfile import TemporaryFile
from sys import exc_info
import os

# Initialize the context.
zmq_context = zmq.Context()
sender_id = uuid4().hex
mongrel_conn = handler.Connection( sender_id, 'tcp://127.0.0.1:5561', 'tcp://127.0.0.1:5562' )

while True:
  req = mongrel_conn.recv()

  # Parse the token from the URI
  my_uri = req.headers[u'URI'].encode('ascii')
  unverified_token = my_uri.split('/')[2]
  good_token = False

  # Ensure the token is valid.
  with TemporaryFile() as temp:
    subprocess.call(['curl','-LI','http://www.vimeo.com/'+str(unverified_token)],stdout=temp)
    temp.seek(0)
    vimeo_response = temp.read()
    vimeo_lines = vimeo_response.split('\n')
    if 'HTTP/1.0 404 Not Found\r' not in vimeo_lines:
      good_token = True

  # What is playlist_str?
  playlist_str = ''
  with TemporaryFile() as temp:
    subprocess.call(['curl','http://www.iqueue.tv/playlists/default/'],stdout=temp)
    temp.seek(0)
    playlist_str = temp.read()

  if playlist_str != '':
    try:
      init_playlist_dict = json.loads( playlist_str )
      proc_playlist_dict = {}
      for k in init_playlist_dict.keys():
        if type(k) == unicode:
          v = init_playlist_dict[k]
          if type(v) == unicode:
            proc_playlist_dict[k.encode('ascii')] = v.encode('ascii')
          else:
            proc_playlist_dict[k.encode('ascii')] = v
        else:
          if type(v) == unicode:
            proc_playlist_dict[k] = v.encode('ascii')
          else:
            proc_playlist_dict[k] = v
    except:
      error = str(exc_info()[1])
      sys.stderr.write ("error: "+error)

  int_token_playlist = []
  for token in proc_playlist_dict['playlist']:
    int_token_playlist.append(int(token))
  proc_playlist_dict['playlist'] = int_token_playlist

  if good_token:
    int_token_playlist.reverse()
    int_token_playlist.append(int(unverified_token))
    int_token_playlist.reverse()
    proc_playlist_dict['playlist'] = int_token_playlist

  file = open('/home/deployment/iqueue.tv/featured.html','r')
  fs = file.read()
  file.close()

  index_1 = fs.index('playlist=[')
  index_2 = index_1+fs[index_1:].index(']')+1
  fs=fs[:index_1] + 'playlist='+str(int_token_playlist) + fs[index_2:]

  mongrel_conn.reply_http( req, fs )
