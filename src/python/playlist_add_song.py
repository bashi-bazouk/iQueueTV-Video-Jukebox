import zmq
from mongrel2 import handler
import json
from uuid import uuid4
from db.songs import *
from random import randint, shuffle
from subprocess import call
from maintenance.token_check import check

# Initialize the context.
zmq_context = zmq.Context()
sender_id = uuid4().hex
mongrel_conn = handler.Connection( sender_id, 'tcp://127.0.0.1:8894', 'tcp://127.0.0.1:8895' )

# Print requests to output until you crash.
while True:
    req = mongrel_conn.recv()

    song_token = ''
    sont_title = ''
    song_artist = ''
    song_album = ''
    song_director = ''
    song_label = ''

    body = str( req.body )
    parts = body.split('&')
    #for part in parts:
    #  print str( part.split('=') )
    for part in parts:
      #print 'part1: '+str( part.split('=')[0] )+', type: '+str( type( part.split('=')[0]))+', list: '+str( list( part.split('=')[0] ) )
      #print 'part2: '+str( part.split('=')[1] )+', type: '+str( type( part.split('=')[1]))+', list: '+str( list( part.split('=')[1] ) )
      if part.startswith('playlist_name'):
        #print str( part )
        playlist_name = str( part.split('=')[1] )
        #print playlist_name
      elif part.startswith( 'submit' ):
        pass
      elif part.split('=')[1] == '':
        #print part.split('=')[0]
        pass
      else:
        #print str( int( part.split('=')[1] ))
        videos.append( int( part.split('=')[1] ) )

    #print playlist_name

    if playlist_exists( playlist_name ):
      for token in videos:
        print 'token: ' + str(token) + ', type: ' + str( type( token ) )
        _token_in_playlist = token_in_playlist( playlist_name, token )
        _token_valid = check( int(token) )
        if ( ( not _token_in_playlist ) and _token_valid ):
          add_token_to_playlist( playlist_name, token )
        else:
          print 'token in playlist: ' + str( _token_in_playlist )
          print 'token valid: ' + str( _token_valid )
      my_str = str( playlist_name ) + '\n' + str( videos )

    else:
      my_str = 'couldn\'t add songs to playlist: ' + str(playlist_name)

    mongrel_conn.reply_http( req, my_str )
