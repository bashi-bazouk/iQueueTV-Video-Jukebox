###
VideoStream Class
###

class VideoStream
  constructor: (@element) ->
    return null if not @element?
  
  @virtual: (name) => () -> alert (this+"."+name+" is not implemented.")
  
  on_play: @virtual "on_play"
  on_playback: @virtual "on_playback"
  on_data: @virtual "on_data"
  on_finish: @virtual "on_finish"
  on_ready: @virtual "on_ready"
  preload: @virtual "preload"
  play: @virtual "play"
  pause: @virtual "pause"

class VimeoStream extends VideoStream
  constructor: (@id) ->
    return null if not @id?
    @element = 
      $("""
        <iframe id="#{@id}" class="vimeo loading" src="http://player.vimeo.com/video/#{@id}?title=0&amp;byline=0&amp;portrait=0&amp;autoplay=0&amp;api=1&amp;player_id=#{@id}" frameborder="0"></iframe>
        """)[0]
    @player = ($f @element)
    @api = @player.api
    @add_event = @player.addEvent
    @remove_event = @player.removeEvent

  with_arg: (arg) => (callback) =>
    if arg == "duration"
      if @duration?
        callback()
      else
        @api 'getDuration', (data) ->
          @duration = data
          callback()
    else if arg == "playing"
      @api 'paused', (paused) ->
        this.playing = not paused
        callback()
    else 
      alert "something went wrong"

  @_set_handler: (name) => (handler) ->
    @add_event name, handler
  on_play:     @_set_handler 'play'
  on_playback: @_set_handler 'playProgress'
  on_data:     @_set_handler 'loadProgress'
  on_finish:   @_set_handler 'finish'
  on_ready:    @_set_handler 'ready'

  preload: () =>
    @on_ready () ->
      @on_play () ->
        @pause()
        @remove_event 'play'
      @play

  play:  () => @on_ready () => @api "play"
  pause: () => @on_ready () => @api "pause"
  toggle_play: () =>
    toggle = () => if playing then @pause() else @play()
    @on_ready () =>
      (@with_arg "playing") toggle

###
MetaData
###

class MetaData
  constructor: (data) ->
    return null if not data?
    @title = data.title
    @artist = data.artist
    @director = data.director
    @label = data.label
    @element = 
      $("""
        <div class="footer"><div id="info"><span id="artist">#{@artist}</span> - <span id="title">#{@title}</span><br><span id="director">#{@director}</span><br><span id="label">#{@label}</span></div><img id="logo" src="http://iqueue.tv/logo.png"></div>
        """)[0]

###
Display
###

class Display
  constructor: (@stream, @metadata) ->
    @element = $('<div class="video">'+@metadata.element+@stream.element+"</div>")[0]

###
Playlist
###

class Playlist
  constructor: (data) ->
    return null if not data?
    @name = data.name
    @ids = data.playlist
    @next_playlist = data.next

  next: () -> @ids.shift()

###
Server
###

class Server
  @get_playlist: (name, callback) ->
    getJSON "http://iqueue.tv/playlist/#{name}/s", '', (data) ->
      callback (new Playlist data)

  @get_meta_data: (id, callback) ->
    getJSON "http://iqueue.tv/video/#{id}", '', (data) ->
      callback (new MetaData data)

###
Video Queue
###

class Queue
  constructor: (@self) ->
    return null if @self?

  @get_primary_queue: () ->
    self = $('#queue')
    if self?
      new Queue(self)
    else
      null

  enqueue: (display) ->
    @self.append display

  dequeue: () ->
    @self.children(".display:first-child").remove()

  clear_queue: () ->
    @self.children(".display").remove()

  get_current_display: () ->
    @self.children(".display:first-child")
      
###
CONFIGURATION AND STATE
###

config =
  buffer: 3

state = 
  now_playing: ___now_playing
  playlist: ___playlist
  next_playlist: "tagged"

push_state = () ->
  urlize = (str) -> str.replace(new RegExp(" ","g"),"_")
  slug = urlize(artist())+"-"+urlize(title())
  history.pushState state, "", "../../playing/"+slug

window.onpopstate = (event) ->
  if event.state?
    state.playlist = event.state.playlist
    state.playlist.unshift (event.state.now_playing)
    clear_queue()
    controller.skip()

###
Controller
###
      
class Controller
  constructor: (@queue) ->
    
    # Define Handlers
    on_document_ready = () =>
      drop_banner = () ->
        $("#overlay").animate { "opacity": 0 }, 300
      @skip()
      setTimeout drop_banner, 3000  

    on_keydown = (data) =>
      switch data.keyCode
        when 13 then @skip()
        when 32 then VideoStream.get_current_stream().toggle_play()
        else false

    on_ajax_error = (XMLHttpRequest,textStatus,errorThrown) ->
      alert errorThrown

    # Set Handlers
    $(document).ready = on_document_ready
    $(document).keydown = on_keydown
    $.ajaxSetup({"error": on_ajax_error})


  # Video Handlers
  track_download: (player) -> (data) ->
    if data.percent > 0.9 and ($ player.element).hasClass "loading"
      player.removeEvent "loadProgress"
      $(player.element).removeClass "loading"
      @queue.enqueue()

  track_playback: (player) => (data) ->
    (player.with_arg "duration") () =>
      if data.seconds > (duration-10) and not $(player.element).hasClass "ending"
        $(player.element).addClass "ending"
        flash_footer()
      if data.seconds - duration < 1
        player.removeEvent 'playProgress'
        @skip()

  skip: () ->
    @queue.dequeue()
    @queue.enqueue () ->
      video = VideoStream.get_current_stream()
      video.on_data (@track_download video)
      video.on_playback (@track_playback video)
      video.on_finish @skip
      video.play()
      

controller = new Controller (new Queue $("#queue"))