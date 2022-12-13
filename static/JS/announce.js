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

    let data = {
        "clubid": clubid,
        "announcement": announcement
    };

    // Handle announcement
    fetch("/send_announce",
        {method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)})
    .then((response) => response.text())
    .then((text) => {
        if (text=="success") {
            alert("Successfully sent your announcement!")
            location.href = "/profile";
        }
        else {
            alert("Error - unable to send announcement")
    }
    });

}

