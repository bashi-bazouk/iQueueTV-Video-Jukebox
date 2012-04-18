import zmq
from mongrel2 import handler
import json
from uuid import uuid4
from random import shuffle
from db.playlists import *

# Initialize the context.
zmq_context = zmq.Context()
sender_id = uuid4().hex
conn = handler.Connection( sender_id, 'tcp://127.0.0.1:7778', 'tcp://127.0.0.1:7779' )

playlists_connection()

# Print requests to output until you crash.
while True:
    req = conn.recv()
    fd = open('../iqueue.tv/new.html','r')
    fs = fd.read()
    fd.close()

    new_json = get_playlist( 'new' )

    #new should always be shuffled
    shuffle( new_json['playlist'] )

    print new_json

    index1 = fs.index('playlist=[')
    index2 = index1+fs[index1:].index(']')
    fs = fs[:(index1+9)] + str( new_json['playlist'] ) + fs[(index2+1):]
 
    response = ''
    response += fs

    conn.reply_http( req, response )
