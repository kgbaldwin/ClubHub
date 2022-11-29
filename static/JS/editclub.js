
window.onload = fillfields;

function new_officer() {
    let clubid = document.getElementById("clubid").value;
    let newofficer = document.getElementById("newofficer").value;

    fetch("/add_officer?newofficer="+newofficer+"&clubid="+clubid)
    .then((response) => response.text())
    .then((text) => {
        var out = text;
        alert(out)
        if (out == "invalid netid") {
            alert("invalid netid")
        }

    });
}

function update_data() {
    alert("update data")
    let mission = document.getElementById("clubmission").value;
    let goals = document.getElementById("clubgoals").value;
    let email = document.getElementById("clubemail").value;
    let insta = document.getElementById("clubinstagram").value;
    let youtube = document.getElementById("clubyoutube").value;
    let imlink = document.getElementById("clubimlink").value;

    const form = new FormData(document.getElementById('editform'));
    fetch('/edit_club_info', {
        method: 'POST',
        body: form
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