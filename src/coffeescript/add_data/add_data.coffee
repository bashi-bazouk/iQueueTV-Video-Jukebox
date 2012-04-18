###
Globals
###

playlist = [36728115]
next_playlist = "default"

current_player = () ->
  element = $(".vimeo:first-child")[0]
  if element?
    $f element
  else
    element

queue_capacity = 3

when_ready = (f) ->
  player = current_player()
  if player?
    player.addEvent 'ready', f
  else
    setTimeout (() -> (when_ready f)), 1000

try_enqueue = () ->
  buffered = $(".vimeo").length
  needMore = buffered < queue_capacity
  _enqueue() if needMore

###
Player Type
###

init_player = (playerID) ->
  $f $("""
       <iframe
         id="#{playerID}"
         class="vimeo loading"
         src="http://player.vimeo.com/video/#{playerID}?title=0&amp;byline=0&amp;portrait=0&amp;autoplay=0&amp;api=1&amp;player_id=#{playerID}"
         frameborder="0">
         </iframe>'
      """)[0]

preload_player = (player) ->
  player.api 'ready', () ->
    player.addEvent 'play', () ->
      player.api 'pause'
      player.removeEvent 'play'
    player.api 'play'
    player.addEvent 'loadProgress', (_track_download player)

_track_download = (player) -> (data) ->
  if data.percent > 0.975
    ($f $(".loading")[0]).removeEvent 'loadProgress'
    ($ player.element).removeClass "loading"
    try_enqueue()

_track_playback = (player) -> (data) ->
  if data.percent > 0.99
    ($ player.element).removeEvent 'playProgress'
    play_next()

toggle_play = () ->
  player = current_player()
  player.addEvent 'ready', () ->
    player.api 'paused', (e) ->
      if e
        player.api 'play'
      else
        player.api 'pause'

###
Player Stack
###

_enqueue = () ->
  nextTrack = playlist.shift()
  if nextTrack?
    player = (init_player nextTrack)
    $('#queue').append player.element
    preload_player player
  else
    get_more_tracks _enqueue

_dequeue = () ->
  $(".vimeo:first-child").remove()

play_next = () ->
  _dequeue()
  try_enqueue()
  when_ready () ->
    player = current_player()
    player.api 'play'
    player.addEvent 'playProgress', (_track_playback player)
    player.addEvent 'finish', play_next

###
Playlist Type
###

requestPlaylist = (name, callback) ->
  url = "/playlists/"+name
  success = (data) -> callback data
  $.getJSON url, '', success

_append_response_to_playlist = (data) ->
  playlist = playlist.concat data.playlist
  next_playlist = data.next

_replace_playlist_with_response = (data) ->
  playlist = data.playlist
  next_playlist = data.next

get_more_tracks = (callback) ->
  requestPlaylist next_playlist, (data) ->
    _append_response_to_playlist data
    callback()
      
###
Initialization
###

$('#overlay').keydown (data) ->
  switch data.keyCode
    when 13 then play_next()
    when 32 then toggle_play()
    else false
    
$.ajaxSetup({"error": (XMLHttpRequest,textStatus,errorThrown) ->
  alert (textStatus+": "+errorThrown+": "+XMLHttpRequest.responseText);
  });

###
Main
###
      
$(document).ready () ->
  drop_banner = () ->
    $("#overlay").animate { "opacity": 0 }, 300
  play_next()
  setTimeout drop_banner, 3000
      
