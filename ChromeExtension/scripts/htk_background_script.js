var communicationPort;
var tab;

/* Listen for connection request */
chrome.extension.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.openConnection == "true") {
		tab = sender.tab;
		sendRequestToCloud(request.wikiPage);
		//sendData(tab);
	}
  });

function sendData(tab, data) {
    var tabID = tab.id;
    communicationPort = chrome.tabs.connect(tabID);
    communicationPort.onMessage.addListener(receiveMessage);
    communicationPort.postMessage({ keyWord : "the", content : data });
}



function receiveMessage(msg) {
}

function sendRequestToCloud(wikiPage) {
	var requestUrl = "http://ec2-50-17-87-12.compute-1.amazonaws.com:8080/cgi-bin/tweetSearch.py?" +
					 "urllink=" + wikiPage;
	alert("Ping cloud");
	$.get(
		requestUrl, 		/* cloud url */
		{},					/* send nothing to cloud */
		/* handle response */
		function(dataReceived) {
			parseCloudData(dataReceived);
		});
		//"json");
}

function parseCloudData(data) {
	sendData(tab, data);
}