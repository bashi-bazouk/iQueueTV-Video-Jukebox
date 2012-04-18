import zmq
from mongrel2 import handler
import json
from uuid import uuid4
import pymongo
from random import randint, shuffle

# Initialize the context.
zmq_context = zmq.Context()

sender_id = uuid4().hex

mongrel_conn = handler.Connection( sender_id, 'tcp://localhost:5559', 'tcp://localhost:5560' )

mongodb_connection_params = ''
mongodb_conn = pymongo.connection.Connection( )

db = mongodb_conn.local
playlist_collection = db.playlists

# Print requests to output until you crash.
while True:
    req = mongrel_conn.recv()

    playlists = playlist_collection.find()
    playlist_count = playlists.count()

    playlist_index = randint( 0, playlist_count-1 )
    single_playlist = playlists[playlist_index]

    if ((single_playlist[u'name'] == u'retired') or (single_playlist[u'name'] == u'new')):
        while ((single_playlist[u'name'] == u'retired') or (single_playlist[u'name'] == u'new')):
            playlist_index = randint( 0, playlist_count-1 )
            single_playlist = playlists[playlist_index]

    py_playlist = single_playlist
    del py_playlist[u'_id']

    shuffle(py_playlist['playlist'])
 
    this_playlist = json.dumps( py_playlist )

    response = ''
    response += str( this_playlist )

    mongrel_conn.reply_http( req, response )
