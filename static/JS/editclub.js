
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

    const form = new FormData(document.getElementById('editform'));
    fetch('/edit_club_info', {
        method: 'POST',
        body: form
    }).then((response) => response.text())
    .then((text) => {
        
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


