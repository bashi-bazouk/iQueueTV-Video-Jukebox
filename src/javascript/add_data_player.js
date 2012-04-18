var current_player, get_more_tracks, init_player, next_playlist, play_next, playlist, preload_player, queue_capacity, requestPlaylist, showBanner, spinBanner, toggle_play, try_enqueue, when_ready, _append_response_to_playlist, _dequeue, _enqueue, _replace_playlist_with_response, _track_download, _track_playback;

playlist = [34389916];

next_playlist = ___next_playlist;

current_player = function() {
  var element;
  element = $(".vimeo:first-child")[0];
  if (element != null) {
    return $f(element);
  } else {
    return element;
  }
};

queue_capacity = 3;

when_ready = function(f) {
  var player;
  player = current_player();
  if (player != null) {
    return player.addEvent('ready', f);
  } else {
    return setTimeout((function() {
      return when_ready(f);
    }), 1000);
  }
};

try_enqueue = function() {
  var buffered, needMore;
  if ($(".loading").length > 0) return;
  buffered = $(".vimeo").length;
  needMore = buffered < queue_capacity;
  if (needMore) return _enqueue();
};

/*
Player Type
*/

init_player = function(playerID) {
  return $f($("<iframe\n  id=\"" + playerID + "\"\n  class=\"vimeo loading\"\n  src=\"http://player.vimeo.com/video/" + playerID + "?title=0&amp;byline=0&amp;portrait=0&amp;autoplay=0&amp;api=1&amp;player_id=" + playerID + "\"\n  frameborder=\"0\">\n  </iframe>'")[0]);
};

preload_player = function(player) {
  return player.api('ready', function() {
    player.addEvent('play', function() {
      player.api('pause');
      return player.removeEvent('play');
    });
    return player.api('play');
  });
};

_track_download = function(player) {
  return function(data) {
    if (data.percent > 0.9 && ($(player.element)).hasClass("loading")) {
      player.removeEvent("loadProgress");
      ($(player.element)).removeClass("loading");
      return try_enqueue();
    }
  };
};

_track_playback = function(player) {
  return function(data) {
    if (data.percent > 0.99) {
      player.removeEvent('playProgress');
      return play_next();
    }
  };
};

toggle_play = function() {
  var player;
  player = current_player();
  return player.addEvent('ready', function() {
    return player.api('paused', function(e) {
      if (e) {
        return player.api('play');
      } else {
        return player.api('pause');
      }
    });
  });
};

/*
Player Stack
*/

_enqueue = function() {
  var nextTrack, player;
  nextTrack = playlist.shift();
  if (nextTrack != null) {
    player = init_player(nextTrack);
    $('#queue').append(player.element);
    return preload_player(player);
  } else {
    return get_more_tracks(_enqueue);
  }
};

_dequeue = function() {
  return $(".vimeo:first-child").remove();
};

play_next = function() {
  _dequeue();
  try_enqueue();
  return when_ready(function() {
    var player;
    player = current_player();
    player.api('play');
    player.addEvent('playProgress', _track_playback(player));
    player.addEvent('loadProgress', _track_download(player));
    return player.addEvent('finish', play_next);
  });
};

/*
Playlist Type
*/

requestPlaylist = function(name, callback) {
  var success, url;
  url = "/playlist/" + name + "/s";
  success = function(data) {
    return callback(data);
  };
  return $.getJSON(url, '', success);
};

_append_response_to_playlist = function(data) {
  playlist = playlist.concat(data.playlist);
  return next_playlist = data.next;
};

_replace_playlist_with_response = function(data) {
  playlist = data.playlist;
  return next_playlist = data.next;
};

get_more_tracks = function(callback) {
  return requestPlaylist(next_playlist, function(data) {
    _append_response_to_playlist(data);
    return callback();
  });
};

/*
Initialization
*/

$(document).keydown(function(data) {
  switch (data.keyCode) {
    case 13:
      return play_next();
    case 32:
      return toggle_play();
    default:
      return false;
  }
});

$.ajaxSetup({
  "error": function(XMLHttpRequest, textStatus, errorThrown) {
    return alert(textStatus + ": " + errorThrown + ": " + XMLHttpRequest.responseText);
  }
});

/*
Banners
*/

showBanner = function(str) {
  return document.title = str;
};

spinBanner = function() {
  var stepBanner;
  stepBanner = function() {
    return document.title = document.title.substr(1) + document.title.substr(0, 1);
  };
  return setInterval(stepBanner, 300);
};

/*
Main
*/

$(document).ready(function() {
  var drop_banner;
  showBanner("iQueueTV                    .");
  spinBanner();
  drop_banner = function() {
    return $("#overlay").animate({
      "opacity": 0
    }, 300);
  };
  play_next();
  return setTimeout(drop_banner, 3000);
});
