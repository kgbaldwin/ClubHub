//'use strict'

function sendAnnouncement() {
    // Get club id and announcement text from user
    announce_club = document.getElementById("clubid");
    let clubid = announce_club.value;
    let announcement = document.getElementById("announcetext").value;

    // User attempts to send empty announcement
    if (announcement == "") {
        alert("Please enter an announcement")
        return
    }

    alert(clubid)
    alert(announcement)

    let data = {
        "clubid": clubid,
        "announcement": announcement
    };

    // Handle announcement
    fetch("/send_announce", 
        {method: 'POST', 
        body: data})
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

