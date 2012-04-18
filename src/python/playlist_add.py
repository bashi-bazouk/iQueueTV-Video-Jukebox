import zmq
from mongrel2 import handler
import json
from uuid import uuid4
from db.playlists import *
from random import randint, shuffle

# Initialize the context.
zmq_context = zmq.Context()
sender_id = uuid4().hex
mongrel_conn = handler.Connection( sender_id, 'tcp://127.0.0.1:7763', 'tcp://127.0.0.1:7764' )

playlists_connection()

# Print requests to output until you crash.
while True:
    req = mongrel_conn.recv()
   
    playlist_name = req.headers[u'URI'].encode('ascii').split('/')[2]
    #print 'playlist_name = ' + str( playlist_name)

    created = new_playlist( playlist_name )
    
    if created:
      fd = open('/home/deployment/iqueue.tv/add_songs_form.html','r')
      response = fd.read()
      fd.close()
    else:
      response = 'couldn\'t create playlist'

    mongrel_conn.reply_http( req, response )
