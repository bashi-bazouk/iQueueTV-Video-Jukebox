import json
import subprocess
import pymongo
from sys import exc_info
from stringify import playlist_string
from tempfile import TemporaryFile

def check( playlist_name ):
  connection = pymongo.Connection()
  db = connection.local
  collection = db.playlists

  playlist = collection.find_one({'name':playlist_name})
  print 'type: '+str(type(playlist))
  playlist = playlist_string( playlist )

  tokens = playlist['playlist']
  post_tokens = []
  retired_tokens = []

  tokens_length = len( tokens )

  for token in tokens:
    curl_results = ''
    with TemporaryFile() as temp:
      subprocess.call(['curl','-IL',('http://www.vimeo.com/'+str(token))],stdout=temp)
      temp.seek(0)
      curl_results = temp.read()

    curl_result_lines = curl_results.split('\n')
    good_link = False
    if 'HTTP/1.0 404 Not Found\r' in curl_result_lines:
      pass
    else:
      good_link = True

    if good_link:
      post_tokens.append( token )
    else:
      retired_tokens.append( token )

  collection.update({'name':playlist_name},{'$set':{'playlist':post_tokens}})

  retired = collection.find_one({'name':'retired'})
  existing_retired_tokens = retired['tokens']
  for token in retired_tokens:
    existing_retired_tokens.append(token)
  collection.update({'name':'retired'},{"$set":{'playlist':existing_retired_tokens}})

  print 'post_tokens: ' + str( post_tokens )
  print 'tokens_length: ' + str(tokens_length)
  print 'post_tokens_length: ' + str(len(post_tokens))
