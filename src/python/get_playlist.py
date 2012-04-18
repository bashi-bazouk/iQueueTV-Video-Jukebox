import zmq
from mongrel2 import handler
import json
from uuid import uuid4
from random import randint, shuffle
from db.playlists import *

# Initialize the context.
zmq_context = zmq.Context()
sender_id = uuid4().hex
mongrel_conn = handler.Connection( sender_id, 'tcp://127.0.0.1:7765', 'tcp://127.0.0.1:7766' )

playlists_connection()

# Print requests to output until you crash.
while True:
    req = mongrel_conn.recv()

    playlist_name = req.headers[u'URI'].encode('ascii').split('/')[2]

    shuffle_on = False
    try:
      shuffle_bit = req.headers[u'URI'].encode('ascii').split('/')[3]
      if shuffle_bit == 's':
        shuffle_on = True
    except:
      pass

    playlist = get_playlist( playlist_name )
    py_playlist = playlist
    del py_playlist[u'_id']
    if shuffle_on or playlist_name == 'default':
      shuffle( py_playlist['playlist'] )
    this_playlist = json.dumps( py_playlist )
    response = ''
    response += str( this_playlist )
    mongrel_conn.reply_http( req, response )
