import pymongo
from sys import exc_info

class dbo():
  '''dbo is a database connection object'''
  def __init__( self ):
    '''starts a connection with the local db'''
    try:
      self.connection = pymongo.Connection()
    except:
      print 'initialization error: ' + str( exc_info()[1] )

  def this_db( self, db_name='local' ):
    '''sets the db we're hooking up to, default is "local"'''
    try:
      self.db = self.connection[db_name]
    except:
      print 'database access error: ' + str( exc_info()[1] )

  def this_collection( self, coll_name ):
    '''sets the collection, no default'''
    try:
      self.collection = self.db[coll_name]
    except:
      print 'collection access error: ' + str( exc_info()[1] )

  #Collection ops
  def get_record( self, key, value ):
    '''returns a record, which is a python dict, or prints error msg'''
    try:
      record = self.collection.find_one( { key : value } )
      return record
    except:
      print 'error retrieving record: ' + str( exc_info()[1] )

  def exists( self, key, value ):
    '''tests whether a given record exists based on a key value pair that should match'''
    try:    
      a = self.collection.find_one( { key : value } )
    except:
      print 'error checking record: ' + str( exc_info()[1] )
    if a == None:
      return False
    else:
      return True

  def insert_record( self, record ):
    '''inserts a python dict into the current collection in the database'''
    success = False
    if type(record) != dict:
      print 'record is not a dict.'
    else:
      self.collection.insert( record )
      success = True
    return success

  def change( self, search_key, search_value, update_key, update_value ):
    try:
      #print 'update_value: ' + str( update_value ) #debug 
      self.collection.update( { search_key : search_value }, {'$set': { update_key : update_value } } )
    except:
      print 'error changing record: ' + str( search_key ) + ':' + str( search_value ) + '\n' + str( exc_info()[1] )

  def remove( self, key, value ):
    try:
      self.collection.remove( { key : value } )
    except:
      print 'error deleting record: ' + str( key ) + ':' + str( value ) + '\n' + str( exc_info()[1] )

  def disconnect( self ):
    try:
      self.connection.disconnect()
    except:
      print ''
