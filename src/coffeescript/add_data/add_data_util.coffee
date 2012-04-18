with_playlist = (name, callback) ->
  $.ajax
    url: "/playlists/"+name,
    dataType: 'json',
    async: false,
    success: callback

with_oembed = (id, callback) ->
  $.getJSON "http://vimeo.com/api/oembed.json?url=http%3A//vimeo.com/#{id}", callback