
window.onload = fillfields;

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
    if (mission != "None") {
        document.getElementById("clubgoals").value = goals;
    }
    if (mission != "None") {
        document.getElementById("clubemail").value = email;
    }
    if (mission != "None") {
        document.getElementById("clubinstagram").value = instagram;
    }
    if (mission != "None") {
        document.getElementById("clubyoutube").value = youtube;
    }
    if (imlink != "None") {
        document.getElementById("clubimlink").value = imlink;
    }

    })
}