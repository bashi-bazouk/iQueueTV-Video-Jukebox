from dbo import dbo
from sys import exc_info

def playlists_connection():
  '''this method connects to the playlists collection and returns collection
  object.'''
  connection = dbo()
  connection.this_db( 'local' )
  connection.this_collection( 'playlists' )
  return connection

def playlist_exists( playlist_name ):
  '''this method checks to see if a playlist with a given name exists already'''
  try:
    connection = playlists_connection()
    exists = connection.exists( 'name', playlist_name )
    connection.disconnect()
    return exists
  except:
    print 'error checking if playlist exists: ' + str( exc_info()[1] )

def new_playlist( playlist_name, playlist=[], next='default' ):
  '''this method adds a new playlist if there is no existing playlist with
  the desired playlist name.'''
  if playlist_exists( playlist_name ):
    print 'there is already a playlist named: ' + str( playlist_name )
    return False
  else:
    try:
      connection = playlists_connection()
      connection.insert_record( { 'name' : playlist_name, 'playlist' : playlist, 'next' : next } )
      connection.disconnect()
      return True
    except:
      print 'error inserting new playlist: ' + str( playlist_name )
      print str( exc_info()[1] )
      return False

def token_in_playlist( playlist_name, token ):
  '''this method checks a given playlist for a token, returns true if the
  token is already in the playlist'''
  if not playlist_exists( playlist_name ):
    print 'there is no existing playlist named: ' + str( playlist_name )
  else:
    try:
      connection = playlists_connection()
      this_playlist_entry = connection.get_record( 'name', playlist_name )
      connection.disconnect()
      this_playlist = this_playlist_entry['playlist']
      token_in_playlist = False
      #print 'this_playlist:' + str(this_playlist) + str(type(this_playlist))
      try:
        this_playlist = eval( this_playlist.encode('ascii') )
      except:
        this_playlist = this_playlist
      #print 'this_playlist:' + str(this_playlist) + str(type(this_playlist))
      #print 'token: ' + str(token)+str(type(token)) #debug
      for i in this_playlist:
        #print str(i)+str(type(i)) #debug
        if int(i) == int(token):
          token_in_playlist = True
          break
      return token_in_playlist
    except:
      print 'error checking if token in playlist: ' + str( exc_info()[1] )

def add_token_to_playlist( playlist_name, token, redundancies=False ):
  '''this method adds a token to the playlist, if it's not already in the playlist'''
  if not playlist_exists( playlist_name ):
    print 'there is no existing playlist named: ' + str( playlist_name )
  elif token_in_playlist( playlist_name, token ) and not redundancies:
    print 'token: ' + str( token ) + ' already exists in playlist'
  else:
    try:
      connection = playlists_connection()
      this_playlist_entry = connection.get_record( 'name', playlist_name )
      this_playlist = this_playlist_entry['playlist']
      try:
        this_playlist = eval( this_playlist.encode('ascii') )
      except:
        this_playlist = this_playlist
      this_playlist.append( int(token) )
      #print str( this_playlist ) #debug
      connection.change( 'name', playlist_name, 'playlist', str(this_playlist)  )
      connection.disconnect()
    except:
      print 'error adding token: ' + str( token ) + ' to playlist: ' + str( playlist_name )
      print str( exc_info()[1] )

def remove_token_from_playlist( playlist_name, token ):
  '''this method takes a playlist name and token and deletes the token from the
  playlist.'''
  if not playlist_exists( playlist_name ):
    print 'playlist: ' + str( playlist_name ) + ' doesn\'t exist' 
  elif not token_in_playlist( playlist_name, token ):
    print 'token: ' + str( token ) + ' not in playlist'
  else:
    try:
      connection = playlists_connection()
      this_playlist_entry = connection.get_record( 'name', playlist_name )
      this_playlist = this_playlist_entry['playlist']
      this_playlist = eval( this_playlist.encode('ascii') )
      modified_playlist = []
      for i in this_playlist:
        if int(i) != int(token):
          modified_playlist.append(i)
      connection.change( 'name', playlist_name, 'playlist', str(modified_playlist) )
      connection.disconnect()
    except:
      print 'error removing token: ' + str( token ) + ' from playlist: ' + str( playlist_name )

def get_playlist( playlist_name ):
  '''this method queries the database, and returns the playlist from the
  playlist object'''
  if not playlist_exists( playlist_name ):
    print 'playlist: ' + str( playlist_name ) + 'doesn\'t exist.'
  try:
    connection = playlists_connection()
    this_record = connection.get_record( 'name', playlist_name ) 
    connection.disconnect()
    return this_record
  except:
    print 'error getting the playlist'
    print str( exc_info()[1] )

def delete_playlist( playlist_name ):
  '''this method will delete a playlist from the db. (mostly for debug purposes,
  probably disable later)'''
  if not playlist_exists( playlist_name ):
    print 'playlist: ' + str( playlist_name ) + 'doesn\'t exist'
  else:
    connection = playlists_connection()
    connection.remove( 'name', playlist_name )
    connection.disconnect()
