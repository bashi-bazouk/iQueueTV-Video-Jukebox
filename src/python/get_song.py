import zmq
from mongrel2 import handler
import json
from uuid import uuid4
from random import randint, shuffle
from db.songs import *

# Initialize the context.
zmq_context = zmq.Context()
sender_id = uuid4().hex
mongrel_conn = handler.Connection( sender_id, 'tcp://127.0.0.1:8892', 'tcp://127.0.0.1:8893' )

# Print requests to output until you crash.
while True:
    req = mongrel_conn.recv()

    print str( req )

    song_token = req.headers[u'URI'].encode('ascii').split('/')[2]

    try:
      song = get_song( str(song_token) )
      py_song = song
      del py_song[u'_id']
      this_song = json.dumps( py_song )
    except:
      this_song = ''

    response = ''
    if str( this_song ) != '':
      response += str( this_song )
    else:
      response += 'not a valid token'

    mongrel_conn.reply_http( req, response )
