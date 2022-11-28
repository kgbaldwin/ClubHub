
window.onload = fillfields;

function new_officer() {
    let clubid = document.getElementById("clubid").value;
    let newofficer = document.getElementById("newofficer").value;

    fetch("/add_officer?newofficer="+newofficer+"&clubid="+clubid)
    .then(() => {location.reload();})
}

function update_data() {
    alert("update data")
    let mission = document.getElementById("clubmission");
    let goals = document.getElementById("clubgoals");
    let email = document.getElementById("clubemail");
    let insta = document.getElementById("clubinstagram");
    let youtube = document.getElementById("clubyoutube");
    let imlink = document.getElementById("clubimlink");
    alert("bouta POST up")
    $.ajax({
        url: '/edit_club_info',
        type: 'POST',
        data: {
            mission: mission,
            goals: goals,
            email: email,
            instagram: insta,
            clubyoutube: youtube,
            imlink: imlink
        },
        success: function(msg) {
            alert('Info updated!');
        }               
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