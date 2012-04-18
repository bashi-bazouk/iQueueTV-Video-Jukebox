class Queue

  constructor: (playlist) ->
    @collection = []
    @load playlist

  load: (name) =>
    with_playlist name, (data) =>
      @enqueue_all data.playlist
      @next_playlist = data.next

  enqueue: (id) =>
    @collection.push (new Player id)

  enqueue_all: (ids) =>
    @enqueue id for id in ids

  dequeue: () =>
    val = @collection.shift()
    @load @next_playlist if @collection.length == 0
    val