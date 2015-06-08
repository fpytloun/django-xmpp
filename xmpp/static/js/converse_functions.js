$(document).ready(function() {
	$("*[data-require=conversejs]").hide();

	require(['converse'], function (converse) {
		// Converse event callbacks
		converse.listen.on('ready', function (event) {
			// When Converse is initialized, show elements that require it
			$("*[data-require=conversejs]").show();

			// Load auto-join rooms and try to join
			// TODO: hard-coded auto-join URL
			$.getJSON("/xmpp/xhr/autojoin/", function(response) {
				$.each(response, function(key, value) {
					box = converse.rooms.open(value.jid);
					box.minimize();
				});
			});
		});
		$("*[data-require=conversejs]").show();

		converse.listen.on('chatRoomOpened', function(event, chatbox) {
			// Add room into auto join rooms
			var jid = chatbox.getRoomJIDAndNick().split("/")[0];
			// TODO: hard-coded auto-join URL
			$.post("/xmpp/xhr/autojoin/", {'action': 'add', 'jid': jid});
		});

		converse.listen.on('chatBoxClosed', function(event, chatbox) {
			// Remove room from auto join rooms
			try {
				var jid = chatbox.getRoomJIDAndNick().split("/")[0];
				// TODO: hard-coded auto-join URL
				$.post("/xmpp/xhr/autojoin/", {'action': 'remove', 'jid': jid});
			} catch (err) {
				// chatbox is not room so it probably doesn't have
				// getRoomJIDAndNich function
				console.log(err);
			}
		});
	});
});

function converse_add_open(jid, fullname) {
	// Add JID into contacts and open chat
	converse.contacts.add(jid, fullname);
	// TODO: event is triggered too soon before contact is available so this
	// will end up in error :-(
	converse.listen.once('roster', function (event) {
		try {
			converse.chats.open(jid);
		} catch (err) {
			console.log(err);
		}
	});
}

$('a[data-function=converse_add_open]').click(function(e) {
	// Add XMPP contact and open chat window
	e.preventDefault();
	converse_add_open($(this).attr('href'), $(this).attr('data-displayname'));
});

$('a[data-function=converse_muc_join]').click(function(e) {
	// Join MUC and open room window
	e.preventDefault();
	room = converse.rooms.open($(this).attr('href'), $(this).attr('data-displayname'));
	room.maximize();
});
