
function new_officer() {
    let clubid = document.getElementById("clubid").value;
    let newofficer = document.getElementById("newofficer").value;

    fetch("/add_officer?newofficer="+newofficer+"&clubid="+clubid)
    .then((response) => response.text())
    .then((text) => {
        var out = text;
        if (out == "invalid netid") {
            alert("Invalid netid");
        }
        else if (out == "success") {
            location.reload();
            alert("Successfully added " + newofficer + " as officer")
        }
    });
}


function remove_officer() {

    if (confirm("Are you sure you want to resign as an officer? \
If you do so mistakenly, a current officer will have to re-add you.")) {

        let clubid = document.getElementById("clubid").value;

        fetch("/remove_officer?clubid="+clubid)
        .then((response) => response.text())
        .then((text) => {
            var out = text;
            if (out == "invalid netid") {
                alert("Invalid netid")
            }
            else if (out == "success") {
                alert("Successfully removed as officer");
                location.href = "/profile";
            }
        });
    }
}


function update_data() {

    let clubid = document.getElementById("clubid").value;
    let mission = document.getElementById("clubmission").value;
    let goals = document.getElementById("clubgoals").value;
    let imlink = document.getElementById("clubimlink").value;
    let email = document.getElementById("clubemail").value;
    let instagram = document.getElementById("clubinstagram").value;
    let youtube = document.getElementById("clubyoutube").value;

    let data = {
        "clubid": clubid,
        "mission": mission,
        "goals": goals,
        "imlink": imlink,
        "email": email,
        "instagram": instagram,
        "youtube":youtube
    };

    fetch('/edit_club_info', {method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)})
    .then((response) => response.text())
    .then((text) => {
        if (text === "success") {
            alert("Successfully updated info!");
            location.href = '/profile';
        }
        else
            alert("Failed to update club info - please wait a few seconds and try again");
            location.href = '/edit_club?clubid='+clubid;
    });

}


function fillfields() {

    let clubid = document.getElementById("clubid").value;
    fetch("/get_info?clubid="+clubid)
    .then((response) => response.text())
    .then((text) => {
    var info = text.split("`");

    let mission = info[1];
    let goals = info[2];
    let email = info[3];
    let instagram = info[4];
    let youtube = info[5];
    let imlink = info[6];

    if (mission != "None") {
        document.getElementById("clubmission").value = mission;
    }
    if (goals != "None") {
        document.getElementById("clubgoals").value = goals;
    }
    if (email != "None") {
        document.getElementById("clubemail").value = email;
    }
    if (instagram != "None") {
        document.getElementById("clubinstagram").value = instagram;
    }
    if (youtube != "None") {
        document.getElementById("clubyoutube").value = youtube;
    }
    if (imlink != "None") {
        document.getElementById("clubimlink").value = imlink;
    }

    })
}


