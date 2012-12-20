
/* Communication with the background scripts */

var communicationPort = null;

/* Request a connection */
	alert(document.URL);
chrome.extension.sendMessage({ openConnection: "true", wikiPage : document.URL});

function sendMessageBackground() {
	communicationPort.postMessage(
	{
		"ID" : "section_iterator",
		"section" : section,
		"rowIndex" : rowIndex
	});

}

function receiveMessageBackground(msg) {
	var keyWord = msg.keyWord;
	appendContent(msg.keyWord, msg.content);
}

chrome.extension.onConnect.addListener(function(thePort) {
    //user clicked context menu item
    //set up the message passing interface
    communicationPort = thePort;
    communicationPort.onMessage.addListener(receiveMessageBackground);
});

/* Communication with the background scripts */

function markWord(str) {
	return "<a class='ourKeyWord' title='some text'>" + str + "<\/a>";
}

function appendContent(keyWord, data) {
	window.setTimeout(function(){
		var regex = keyWord;
		var re = new RegExp(regex, "gi");
		
		/* Find all occurances of our keyword and mark them. */
		$("body *").replaceText(re, markWord);
		
		/* Add tooltip that will show the twitter data on hover. */
		//document.body.innerHTML += parseHTML(data);
		
		$( ".ourKeyWord" ).tooltip({ 
										content: function() {return parseHTML(keyWord, data);} 
									});
	}, 0);	
}

function parseHTML(keyWord, data) {
	

	return "<div class='toolTipClass'>"
			+	"<div class='tweetContainer'>"
			+		"<h2>Tweets for <span style='color:red;'>" + keyWord + "</span></h2>"
			+	"</div>" 
			
			+	parseTweetsHTML(data)
			
			+"</div>";
}

function parseTweetsHTML(data) {
	var result = "";
	var user;
	var tweet;
	for(var i = 0, len = data.length; i < len; i++) {
		tweet = data[i];
		user = tweet["from_user"];
		result = result +
		"<div class='tweetContainer'>"
		+	"<div class='twitterContent'>"
		+		"<div class='tweetHeader'>"
		+			"<a href='http://www.twitter.com/" + user + "' target='_blank' class='userAnchor'>"
		+				"<strong>" + tweet["from_user_name"] + "</strong>" 
		+				"<span class='userSpan'>"
		+					"<s>@</s>" 
		+					"<b>" + user + "</b>"
		+				"</span>"
		+				"<img class='avatarClass' src='" + tweet["profile_image_url"] + "' alt='Avatar' />"
		+			"</a>"
		+		"</div>"
		+		"<p>"
		+			tweet["text"]
		+		"</p>"
		+	"</div>"
		+"</div>"
		;
	}
	return result;
}