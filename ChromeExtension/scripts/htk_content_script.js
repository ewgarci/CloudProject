
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
		$( ".ourKeyWord" ).tooltip({ 
										content: function() {return parseHTML(data);} 
									});
	}, 0);	
}

function parseHTML(data) {
	return data;
	//return "<div style='color: Red; width:300px; height:100px;'>An awesome html content.</div>";
}