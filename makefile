.PHONY: player.js index.html beta.html


src/javascript/player.js : src/coffeescript/player.coffee 
	coffee -c --bare -o src/javascript/ src/coffeescript/player.coffee
#	uglifyjs --overwrite src/javascript/player.js


player.js : src/javascript/player.js


iqueue.tv/index.html: templates/index.html src/javascript/player.js
	ogdata=`cat templates/ogdata/player` playerJS=`cat src/javascript/player.js` interpolate templates/index.html > temp
	playlist='[]' next_playlist='"new"' finalize temp > iqueue.tv/index.html
	rm temp

index.html : iqueue.tv/index.html



all : index.html player.js add_data.html



src/javascript/add_data_player.js : src/coffeescript/add_data/add_data_player.coffee
	coffee -c --bare -o src/javascript/ src/coffeescript/add_data/add_data_player.coffee
	uglifyjs --overwrite src/javascript/add_data_player.js


add_data_player.js : src/javascript/add_data_player.js



iqueue.tv/add_data.html : templates/add_data.html add_data_player.js
	echo ${PATH}
	ogdata=`cat templates/ogdata/player` add_dataJS=`cat src/javascript/add_data_player.js` interpolate templates/add_data.html > temp
	playlist='[]' next_playlist='"new"' finalize temp > iqueue.tv/add_data.html
	rm temp

add_data.html : iqueue.tv/add_data.html

src/javascript/player-beta.js : src/coffeescript/player-beta.coffee
	coffee -c --bare -o src/javascript/ src/coffeescript/player-beta.coffee
#	uglifyjs --overwrite src/javascript/player-beta.js

iqueue.tv/beta.html: templates/index.html src/javascript/player-beta.js
	ogdata=`cat templates/ogdata/player` playerJS=`cat src/javascript/player-beta.js` interpolate templates/index.html > temp
	now_playing="null" playlist='[]' next_playlist='"new"' finalize temp > iqueue.tv/beta.html
	rm temp

beta.html : iqueue.tv/beta.html