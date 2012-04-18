import json

def playlist_string( unicode_json ):
  init_playlist_dict = unicode_json
  proc_playlist_dict = {}
  for k in init_playlist_dict.keys():
    if type(k) == unicode:
      v = init_playlist_dict[k]
      if type(v) == unicode:
        proc_playlist_dict[k.encode('ascii')] = v.encode('ascii')
      else:
        proc_playlist_dict[k.encode('ascii')] = v
    else:
      if type(v) == unicode:
        proc_playlist_dict[k] = v.encode('ascii')
      else:
        proc_playlist_dict[k] = v

  playlist = []

  playlist_dict = eval( proc_playlist_dict['playlist'] )

  for token in playlist_dict:
    playlist.append( int(token) )

  proc_playlist_dict['playlist'] = playlist

  return proc_playlist_dict
