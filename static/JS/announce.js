//'use strict'

function sendAnnouncement() {

    // Get club id, clubname and announcement text from user
    announce_club = document.getElementById("announceclub");
    let clubid = announce_club.value;
    let clubname = announce_club.options[announce_club.selectedIndex].text;
    let announcement = document.getElementById("announcetext").value

    // User forgets to select a club
    if (clubname == "Choose a club") {
        alert("Please select a club")
        return
    }

    // User attempts to send empty announcement
    if (announcement == "") {
        alert("Please enter an announcement")
        return
    }

    // Handle announcement
    fetch_url = "/send_announce?clubid=" + encodeURIComponent(clubid)
    fetch_url += "&announcement=" + encodeURIComponent(announcement)
    fetch(fetch_url)
    .then((response) => response.text())
    .then((text) => {
        if (text=="success")
            alert("Successfully sent your announcement!")
        else alert("Error - unable to send announcement")
    });

    // Clear the form
    document.getElementById("announceclub").value = "none"
    document.getElementById("announcetext").value = ""

}

