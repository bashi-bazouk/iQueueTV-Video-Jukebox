import zmq
from mongrel2 import handler
import json
from uuid import uuid4
from db.songs import *
from urllib import unquote
from sys import exc_info

# Initialize the context.
zmq_context = zmq.Context()
sender_id = uuid4().hex
mongrel_conn = handler.Connection( sender_id, 'tcp://127.0.0.1:8894', 'tcp://127.0.0.1:8895' )

# Print requests to output until you crash.
while True:
  req = mongrel_conn.recv()

  #print str( req ) #debug

  song_token = ''
  sont_title = ''
  song_artist = ''
  song_album = ''
  song_director = ''
  song_label = ''

  body = str( req.body )
  parts = body.split('&')
  for part in parts:
    #print 'part: ' + str( part )
    if part.startswith('song_token'):
      song_token = unquote( str( part.split('=')[1] ) ).replace('+',' ')
    elif part.startswith('song_title'):
      song_title = unquote( str( part.split('=')[1] ) ).replace('+',' ')
    elif part.startswith('song_artist'):
      song_artist = unquote( str( part.split('=')[1] ) ).replace('+',' ')
    elif part.startswith('song_album'):
      song_album = unquote( str( part.split('=')[1] ) ).replace('+',' ')
    elif part.startswith('song_director'):
      song_director = unquote( str( part.split('=')[1] ) ).replace('+',' ')
    elif part.startswith('song_label'):
      song_label = unquote( str( part.split('=')[1] ) ).replace('+',' ')
    elif part.startswith( 'submit' ):
      pass

  print 'song_token: ' + str( song_token )
  print 'song_title: ' + str( song_title )
  print 'song_artist: ' + str( song_artist )
  print 'song_album: ' + str( song_album )
  print 'song_label: ' + str( song_label )

  #print 'song_exists( str( song_token ) ): ' + str( song_exists( str( song_token ) ) )

  if not song_exists( str( song_token ) ):
    good_token = new_song( song_token )
  else:
    good_token = True

  if good_token:
    song_obj = get_song( str( song_token ) )
    py_song_obj = song_obj
    del py_song_obj[u'_id']
    #print 'song_title: ' + song_title #debug
    if song_title != '':
      py_song_obj[u'title'] = song_title
    #print 'song_artist: ' + song_artist #debug
    if song_artist != '':
      py_song_obj[u'artist'] = song_artist
    #print 'song_director: ' + song_director #debug
    if song_director != '':
      py_song_obj[u'director'] = song_director
    #print 'song_label: ' + song_label #debug
    if song_label != '':
      py_song_obj[u'record_label'] = song_label
    #print 'song_album: ' + song_album #debug
    if song_album != '':
      py_song_obj[u'album'] = song_album

    #print py_song_obj

    update_song( str( song_token ), py_song_obj )

  else:
    print 'token is no good: ' + str( song_token )
  
  response = ''
  a = get_song( str(song_token) )
  #try:
  print a.keys() #debug
  response += '<html><body><link rel="stylesheet" type="text/css" href="/add_data.css"><p>artist: ' + str( a[u'artist'] ) + '<br / >title: ' + str( a[u'title'] ) + '<br />album: ' + str( a[u'album'] ) + '<br />director: ' + str( a[u'director'] ) + '<br />label: ' + str( a[u'record_label'] )
  #except:
  #  print 'debug: ' + str( exc_info()[1] )

  #response  = '<html><body><p>' + str( get_song( str( song_token ) ) ).replace('iframe','_iframe')
  response += '</p><a href="/add_song_data.html">New Song</a></body></html>'
  #with open('/home/deployment/iqueue.tv/add_song_data.html','r') as form:
  #  response = form.read()

  #print 'dir(req): ' + str( dir(req) ) #debug
  #print 'req.headers: ' + str( req.headers ) #debug

  mongrel_conn.reply_http( req, response )
