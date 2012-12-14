
/* Communication with the background scripts */

var communicationPort = null;

/* Request a connection */
chrome.extension.sendMessage({ openConnection: "true", wikiPage : "wikiPageId"});

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
	appendContent(msg.keyWord);
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

function appendContent(keyWord) {
	window.setTimeout(function(){
		var regex = keyWord;
		var re = new RegExp(regex, "gi");
		
		/* Find all occurances of our keyword and mark them. */
		$("body *").replaceText(re, markWord);
		
		/* Add tooltip that will show the twitter data on hover. */
		$( ".ourKeyWord" ).tooltip({ 
										content: function() {return parseHTML();} 
									});
	}, 0);	
}

function parseHTML() {
	return "<div style='color: Red; width:300px; height:100px;'>An awesome html content.</div>";
}

// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.
var req = new XMLHttpRequest();
req.open(
    "GET",
    "http://api.flickr.com/services/rest/?" +
        "method=flickr.photos.search&" +
        "api_key=90485e931f687a9b9c2a66bf58a3861a&" +
        "text=hello%20world&" +
        "safe_search=1&" +  // 1 is "safe"
        "content_type=1&" +  // 1 is "photos only"
        "sort=relevance&" +  // another good one is "interestingness-desc"
        "per_page=20",
    true);
req.onload = showPhotos;
req.send(null);

function showPhotos() {
  var photos = req.responseXML.getElementsByTagName("photo");

  for (var i = 0, photo; photo = photos[i]; i++) {
    var img = document.createElement("image");
    img.src = constructImageURL(photo);
    document.body.appendChild(img);
  }
}

// See: http://www.flickr.com/services/api/misc.urls.html
function constructImageURL(photo) {
  return "http://farm" + photo.getAttribute("farm") +
      ".static.flickr.com/" + photo.getAttribute("server") +
      "/" + photo.getAttribute("id") +
      "_" + photo.getAttribute("secret") +
      "_s.jpg";
}