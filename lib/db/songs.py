from dbo import dbo
from subprocess import call
from tempfile import TemporaryFile
from sys import exc_info
import json

def songs_connection():
  '''this method connects to the songs collection and returns collection
  object.'''
  connection = dbo()
  connection.this_db( 'local' )
  connection.this_collection( 'songs' )
  return connection

def song_exists( song_id ):
  '''this method checks to see if a song with a given id exists already'''
  try:
    connection = songs_connection()
    exists = connection.exists( 'song_id', song_id )
    connection.disconnect()
    return exists
  except:
    print 'error checking if song exists: ' + str( exc_info()[1] )

def new_song( song_id ):
  '''this method adds a new song if there is no existing song with
  the desired song id.'''
  if song_exists( song_id ):
    print 'there is already a song with id: ' + str( song_id )
    return False
  else:
    try:
      try:
        video_token = int( song_id )
        is_int = True
      except:
        print 'video_token ' + str( video_token ) + ' is not int'
        is_int = False
      if is_int:
        video_token = str( video_token )
        response_str = ''

        with TemporaryFile() as temp:
          call( [ 'curl', '-L', ('http://vimeo.com/api/oembed.json?url=http%3A//vimeo.com/'+video_token) ], stdout=temp )
          temp.seek( 0 )
          response_str = temp.read()

        invalid_token = False
        if response_str.startswith( '4' ) or response_str.startswith( '5' ):
          invalid_token = True

        if not invalid_token and not ( response_str == '' ):
          oembed_dict = json.loads( response_str )
          try:
            connection = songs_connection()
            connection.insert_record( { 'song_id' : song_id, 'oembed' : oembed_dict, 'title' : '', 'artist' : '', 'director' : '', 'record_label' : '' } )
            connection.disconnect()
            return True
          except:
            print 'error inserting new song to db:'
            print str( exc_info()[1] )        
            return False
        return False
      return False
    except:
      print 'error inserting new song with id: ' + str( song_id )
      print str( exc_info()[1] )
      return False

def get_song( song_id ):
  '''this method queries the database, and returns the song with the
  matching id'''
  if not song_exists( song_id ):
    print 'song with id: ' + str( song_id ) + ' doesn\'t exist.'
  try:
    connection = songs_connection()
    this_record = connection.get_record( 'song_id', song_id ) 
    connection.disconnect()
    return this_record
  except:
    print 'error getting the song: '
    print str( exc_info()[1] )

def delete_song( song_id ):
  '''this method will delete a song from the db. (mostly for debug purposes,
  probably disable later)'''
  if not song_exists( song_id ):
    print 'song: ' + str( song_id ) + ' doesn\'t exist'
  else:
    try:
      connection = songs_connection()
      connection.remove( 'song_id', song_id )
      connection.disconnect()
    except:
      print 'error removing the song with id: ' + str( song_id )
      print str( exc_info()[1] )

def update_song( song_id, song_obj ):
  '''this method will update the song object specified by the song_id to hold
  the object in song_obj'''

  print str( song_obj ) #debug
  print str(type(song_obj)) #debug

  if not song_exists( song_id ):
    good_token = new_song( song_id )
  else:
    good_token = True

  if good_token:
    try:
      connection = songs_connection()
      for i in song_obj.keys():
        connection.change( 'song_id', song_id, i, song_obj[i] )
      connection.disconnect()
    except:
      print 'error updating song with id: ' + str( song_id )
      print str( exc_info()[1] )

