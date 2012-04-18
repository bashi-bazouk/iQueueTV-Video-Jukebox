import json
import pymongo

def upload_oembed( response, token_str ):
  '''this function takes a response which will be a json obj or a bad response
  code, ie: startswith 4 or 5, and a string reprentation of the vimeo token, 
  and upload the new song to the db'''
  if not (response.startswith('4') or response.startswith('5')):
    oembed_dict = json.loads( response )
    
    #this part sets up the connection
    connection = pymongo.Connection()
    db = connection['local']
    collection = db['songs']

    try:
      record = collection.find_one({'song_id':token_str})
    except:
      collection.insert( { 'song_id':token_str,'oembed':oembed_dict, 'title':'', 'artist':'', 'director':'', 'record_label':'IndieVision' } )

    connection.disconnect()

  else:
    print 'no response for this token'
