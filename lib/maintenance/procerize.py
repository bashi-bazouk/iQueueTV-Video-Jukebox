from subprocess import call
from random import randint
from tempfile import TemporaryFile
import os
import shutil

def procerize( app_file ):
  
  if app_file.endswith( '.py' ):
    py_app_file = app_file
    app_file = app_file[:-3]
  else:
    py_app_file = app_file + '.py'

  mydir = os.path.join( '/home/procer/profiles', app_file )

  try:
    shutil.copytree( '/home/procer/profiles/shuffle-queue', mydir )
  except:
    shutil.rmtree( mydir )
    shutil.copytree( '/home/procer/profiles/shuffle-queue', mydir )

  fd = open( os.path.join( mydir, 'pid_file' ) , 'w')
  fd.write( os.path.join(  mydir, ( app_file + '.pid' ) ) )
  fd.close()

  shutil.move( os.path.join( mydir, 'shuffle-queue.pid' ), os.path.join( mydir, ( app_file + '.pid') ) )

  good_guess = False
  while not good_guess:
    pid_guess = randint( 2000, 20000 )
    with TemporaryFile() as temp:
      call( ['ps','aux'], stdout=temp )
      temp.seek( 0 )
      fs = temp.read()
      if not ( str( pid_guess ) in fs ):
        break

  fd = open( os.path.join( mydir, ( app_file + '.pid' ) ), 'w' )
  fd.write( str( pid_guess ) )
  fd.close()

  fd = open( os.path.join( mydir, 'run' ), 'r+' )
  fs = fd.read()
  fsl = fs.split('\n')
  mod_fsl = []
  for i in fsl:
    try:
      mod_fsl.append( i.replace( 'shuffle-queue', app_file ) )
    except:
      mod_fsl.append( i )
  fd.seek( 0 )
  fd.write( '\n'.join( mod_fsl ) )
  fd.close()

  shutil.copy( os.path.join( mydir, 'run' ), os.path.join( mydir, 'reset' ) )

  call( ['killall', 'procer'] )
  call( ['/home/procer/run_procer'] )

  myfiles = os.listdir( mydir )
  for file_name in myfiles:
    if file_name.endswith( '~' ):
      os.remove( os.path.join( mydir, file_name ) )
