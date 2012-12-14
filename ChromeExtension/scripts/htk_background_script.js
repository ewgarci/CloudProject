var communicationPort;

chrome.extension.onMessage.addListener(
  function(request, sender, sendResponse) {
	var tab = sender.tab;
    console.log(sender.tab ?
                "from a content script:" + sender.tab.url :
                "from the extension");
    if (request.greeting == "hello") {
		addProfessorNames(tab);
	}
  });

function addProfessorNames(tab) {
    var tabID = tab.id;
    communicationPort = chrome.tabs.connect(tabID);
    communicationPort.onMessage.addListener(handleMessage);
    communicationPort.postMessage({"ID" : "add_teachers"});
}

function handleMessage(msg) {
    switch(msg["ID"]) {
        case "section_iterator":
            var section = msg["section"],
                rowIndex = msg["rowIndex"];
                
				lookupSection(section, rowIndex);
	}
}

function sendTeachDataToPage(sectionRowIndex, fullTextName, rateMyProfessorID) {
    communicationPort.postMessage({
        "ID": "add_teacher_data",
        "sectionRowIndex": sectionRowIndex,
        "fullTextName": fullTextName,
        "rateMyProfessorID": rateMyProfessorID
    });
}


function getBestRateMyProfessorTID(lastName, fullTextName, sectionRowIndex) {
    //find the teacher with the name closest to the one specified, as determined by the levenshtein distance
    //not perfect, but should suffice for most cases. the disclaimer will make up for the other cases ;)
    var url = "http://ec2-23-22-84-14.compute-1.amazonaws.com/findteacher.php?lastname=" + lastName;
    $.get(url, {}, function(teachers){
        var i = 0;
            teacherCount = teachers.length,
            bestGuess = null,
            lowestLevenshteinDistance = 100000;
        for (var i = 0; i < teacherCount; i++) {
            var teacherEntry = teachers[i],
                currentFullName = teacherEntry["FullTextName"],
                ld = levenshtein(fullTextName, currentFullName);
            if (bestGuess == null || ld < lowestLevenshteinDistance) {
                lowestLevenshteinDistance = ld;
                bestGuess = teacherEntry;
            }
        }
        if (bestGuess == null) {
            sendTeachDataToPage(sectionRowIndex, fullTextName, null);
        } else {
            sendTeachDataToPage(sectionRowIndex, fullTextName, bestGuess["RateMyProfessorID"]);
        }
    }, "json");
}