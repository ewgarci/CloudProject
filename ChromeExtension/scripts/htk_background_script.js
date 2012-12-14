var communicationPort;

/* Listen for connection request */
chrome.extension.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.openConnection == "true")
		sendData(sender.tab);
  });

function sendData(tab) {
    var tabID = tab.id;
    communicationPort = chrome.tabs.connect(tabID);
    communicationPort.onMessage.addListener(receiveMessage);
    communicationPort.postMessage({ keyWord : "bomb"});
}

function receiveMessage(msg) {

}