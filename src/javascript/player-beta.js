/*
VideoStream Class
*/
var MetaData, VideoStream, artist, clear_queue, config, dequeue, director, enqueue, flash_footer, generate_player_element, get_info, get_more_tracks, get_set_by_id, hide_info, hide_logo, label, play_next, push_state, set_info, show_info, show_logo, state, title, _append_response_to_playlist, _track_download, _track_playback,
  __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

VideoStream = (function() {

  function VideoStream(element) {
    this.element = element;
    this.toggle_play = __bind(this.toggle_play, this);
    this.pause = __bind(this.pause, this);
    this.play = __bind(this.play, this);
    this.preload = __bind(this.preload, this);
    this.with_arg = __bind(this.with_arg, this);
    if (!(this.element != null)) return null;
    this.player = $f(this.element);
    this.api = this.player.api;
    this.add_event = this.player.addEvent;
    this.remove_event = this.player.removeEvent;
  }

  VideoStream.prototype.with_arg = function(arg) {
    var _this = this;
    return function(callback) {
      if (arg === "duration") {
        if (_this.duration != null) {
          return callback();
        } else {
          return _this.api('getDuration', function(data) {
            this.duration = data;
            return callback();
          });
        }
      } else if (arg === "playing") {
        return _this.api('paused', function(paused) {
          this.playing = !paused;
          return callback();
        });
      } else {
        return alert("something went wrong");
      }
    };
  };

  VideoStream._set_handler = function(name) {
    return function(handler) {
      return this.add_event(name, handler);
    };
  };

  VideoStream.prototype.on_play = VideoStream._set_handler('play');

  VideoStream.prototype.on_playback = VideoStream._set_handler('playProgress');

  VideoStream.prototype.on_data = VideoStream._set_handler('loadProgress');

  VideoStream.prototype.on_finish = VideoStream._set_handler('finish');

  VideoStream.prototype.on_ready = VideoStream._set_handler('ready');

  VideoStream.prototype.preload = function() {
    return this.on_ready(function() {
      this.on_play(function() {
        this.pause();
        return this.remove_event('play');
      });
      return this.play;
    });
  };

  VideoStream.prototype.play = function() {
    var _this = this;
    return this.on_ready(function() {
      return _this.api("play");
    });
  };

  VideoStream.prototype.pause = function() {
    var _this = this;
    return this.on_ready(function() {
      return _this.api("pause");
    });
  };

  VideoStream.prototype.toggle_play = function() {
    var toggle,
      _this = this;
    toggle = function() {
      if (playing) {
        return _this.pause();
      } else {
        return _this.play();
      }
    };
    return this.on_ready(function() {
      return (_this.with_arg("playing"))(toggle);
    });
  };

  VideoStream.get_current_stream = function() {
    var element;
    element = $(".vimeo:first-child")[0];
    if (!(element != null)) {
      return null;
    } else {
      return new Player(element);
    }
  };

  VideoStream.generate_document_object = function(video_id) {
    return $("<iframe id=\"" + video_id + "\" class=\"vimeo loading\" src=\"http://player.vimeo.com/video/" + video_id + "?title=0&amp;byline=0&amp;portrait=0&amp;autoplay=0&amp;api=1&amp;player_id=" + video_id + "\" frameborder=\"0\"></iframe>")[0];
  };

  return VideoStream;

}).call(this);

/*
MetaData Class
*/

MetaData = (function() {

  function MetaData(id) {
    this.id = id;
    this.with_arg = __bind(this.with_arg, this);
    this.init = __bind(this.init, this);
    if (!(this.id != null)) return null;
  }

  MetaData.prototype.init = function(callback) {
    var url;
    url = "http://iqueue.tv/video/" + id;
    return $.getJSON(url, '', function(data) {
      this.title = data.title;
      this.artist = data.artist;
      this.director = data.director;
      this.label = data.label;
      return callback();
    });
  };

  MetaData.prototype.with_arg = function(arg) {
    var _this = this;
    return function(callback) {
      if ((eval("this." + arg)) != null) {
        return callback();
      } else {
        return init(function() {
          return (with_arg(arg))(callback);
        });
      }
    };
  };

  return MetaData;

})();

/*
UTILITIES
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
  if (data != null) {
    document.title = data.artist;
    artist(data.artist);
    title(data.title);
    label(data.label);
    return director(data.director);
  }
};

/*
Player Type
*/

generate_player_element = function(playerID) {
  return $("<iframe id=\"" + playerID + "\" class=\"vimeo loading\" src=\"http://player.vimeo.com/video/" + playerID + "?title=0&amp;byline=0&amp;portrait=0&amp;autoplay=0&amp;api=1&amp;player_id=" + playerID + "\" frameborder=\"0\"></iframe>")[0];
};

_track_download = function(player) {
  return function(data) {
    if (data.percent > 0.9 && ($(player.element)).hasClass("loading")) {
      player.removeEvent("loadProgress");
      ($(player.element)).removeClass("loading");
      return enqueue();
    }
  };
};

_track_playback = function(player) {
  return function(data) {
    var _this = this;
    return (player.with_arg("duration"))(function() {
      if (data.seconds > (duration - 10) && !($(player.element)).hasClass("ending")) {
        ($(player.element)).addClass("ending");
        flash_footer();
      }
      if (data.percent > 0.99) {
        player.removeEvent('playProgress');
        return play_next();
      }
    });
  };
};

/*
Player Stack
*/

enqueue = function(callback) {
  var buffered, element, next_track;
  if ($(".loading").length > 0) return;
  buffered = $(".vimeo").length;
  if (buffered < config.buffer) {
    if (!(typeof next_track !== "undefined" && next_track !== null)) {
      next_track = state.playlist.shift();
    }
    if (next_track != null) {
      element = generate_player_element(next_track);
      $('#queue').append(element);
      return callback();
    } else {
      return get_more_tracks((function() {
        return enqueue(callback);
      }));
    }
  }
};

dequeue = function() {
  return $(".vimeo:first-child").remove();
};

clear_queue = function() {};

play_next = function() {
  dequeue();
  return enqueue(function() {
    var player,
      _this = this;
    player = VideoStream.get_current_stream();
    player.play();
    player.on_data(_track_download(player));
    player.on_finish(play_next);
    (player.with_arg("duration"))(function() {
      return player.on_playback(_track_playback(player));
    });
    return get_info(function(data) {
      state.now_playing = data;
      push_state();
      set_info(data);
      return flash_footer();
    });
  });
};

/*
Playlist Type
*/

_append_response_to_playlist = function(data) {};

get_more_tracks = function(callback) {
  var url;
  url = "/playlist/" + state.next_playlist + "/s";
  return $.getJSON(url, '', function(data) {
    state.playlist = state.playlist.concat(data.playlist);
    state.next_playlist = data.next;
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
      return VideoStream.get_current_stream().toggle_play();
    default:
      return false;
  }
});

$.ajaxSetup({
  "error": function(XMLHttpRequest, textStatus, errorThrown) {
    return alert(errorThrown);
  }
});

/*
Information
*/

get_info = function(id) {
  return function(callback) {
    var url;
    url = "/video/" + id;
    return $.getJSON(url, '', callback);
  };
};

flash_footer = function() {
  var missing_information;
  missing_information = function() {
    var not_available;
    not_available = "N/A";
    return title() === not_available || artist() === not_available || (label() === not_available && director() === not_available);
  };
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
CONFIGURATION AND STATE
*/

config = {
  buffer: 3
};

state = {
  now_playing: ___now_playing,
  playlist: ___playlist,
  next_playlist: "tagged"
};

push_state = function() {
  var slug, urlize;
  urlize = function(str) {
    return str.replace(new RegExp(" ", "g"), "_");
  };
  slug = urlize(artist()) + "-" + urlize(title());
  return history.pushState(state, "", "../../playing/" + slug);
};

window.onpopstate = function(event) {
  if (event.state != null) {
    state.playlist = event.state.playlist;
    state.playlist.unshift(event.state.now_playing);
    clear_queue();
    return play_next();
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
