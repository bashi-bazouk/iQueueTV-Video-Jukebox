var artist, current_player, director, flash_footer, get_info, get_more_tracks, get_set_by_id, hide_info, hide_logo, init_player, label, missing_information, next_playlist, play_next, playlist, preload_player, queue_capacity, requestPlaylist, set_info, set_title, show_info, show_logo, step_title, title, toggle_play, try_enqueue, when_ready, with_duration, _append_response_to_playlist, _clear_queue, _dequeue, _enqueue, _replace_playlist_with_response, _track_download, _track_playback;

playlist = ___playlist;

next_playlist = ___next_playlist;

queue_capacity = 3;

/*
UTILITIES
*/

current_player = function() {
  var element;
  element = $(".vimeo:first-child")[0];
  if (element != null) {
    return $f(element);
  } else {
    return element;
  }
};

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

with_duration = function(player, callback) {
  return player.api('getDuration', callback);
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
    step_title();
    if (data.percent > 0.9 && ($(player.element)).hasClass("loading")) {
      player.removeEvent("loadProgress");
      ($(player.element)).removeClass("loading");
      return try_enqueue();
    }
  };
};

_track_playback = function(player, duration) {
  return function(data) {
    if (data.seconds > (duration - 10) && !($(player.element)).hasClass("ending")) {
      ($(player.element)).addClass("ending");
      flash_footer();
    }
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

_clear_queue = function() {
  return $(".vimeo").remove();
};

play_next = function() {
  _dequeue();
  try_enqueue();
  return when_ready(function() {
    var player;
    get_info(function(data) {
      set_info(data);
      return flash_footer();
    });
    player = current_player();
    player.api('play');
    with_duration(player, function(duration) {
      return player.addEvent('playProgress', _track_playback(player, duration));
    });
    player.addEvent('loadProgress', _track_download(player));
    return player.addEvent('finish', play_next);
  });
};

/*
Playlist Type
*/

requestPlaylist = function(name, callback) {
  var success, url;
  url = "http://iqueue.tv/playlist/" + name + "/s";
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
    return 0;
  }
});

/*
Banners
*/

set_title = function(str) {
  return document.title = str;
};

step_title = function() {
  var len;
  len = ($('title').html().length + 1) % 4;
  return $('title').html(Array(len).join('.'));
};

/*
Information
*/

get_set_by_id = function(id) {
  return function(val) {
    if (val != null) {
      return $("#" + id).text(val);
    } else {
      return $("#" + id).text();
    }
  };
};

title = get_set_by_id("title");

artist = get_set_by_id("artist");

label = get_set_by_id("label");

director = get_set_by_id("director");

show_info = function() {
  return $("#info").animate({
    opacity: 1
  }, 300);
};

hide_info = function() {
  return $("#info").animate({
    opacity: 0
  }, 300);
};

show_logo = function() {
  return $("#logo").animate({
    opacity: 1
  }, 300);
};

hide_logo = function() {
  return $("#logo").animate({
    opacity: 0
  }, 300);
};

set_info = function(data) {
  artist(data.artist);
  title(data.title);
  label(data.label);
  return director(data.director);
};

get_info = function(callback) {
  var id, url;
  id = $(".vimeo:first-child").attr("id");
  url = "/video/" + id;
  return $.getJSON(url, '', callback);
};

missing_information = function() {
  var not_available;
  not_available = "N/A";
  return title() === not_available || artist() === not_available || (label() === not_available && director() === not_available);
};

flash_footer = function() {
  if (missing_information()) {
    show_logo();
    return setTimeout(hide_logo, 5000);
  } else {
    show_info();
    setTimeout(hide_info, 5000);
    show_logo();
    return setTimeout(hide_logo, 5000);
  }
};

/*
Main
*/

$(document).ready(function() {
  var drop_banner;
  drop_banner = function() {
    return $("#overlay").animate({
      "opacity": 0
    }, 300);
  };
  play_next();
  return setTimeout(drop_banner, 3000);
});
