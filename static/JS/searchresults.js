//'use strict'

// https://stackoverflow.com/questions/9618504/how-to-get-the-selected-radio-button-s-value
//document.querySelector('input[name="clubname"]:checked').value;

function changeInfo() {

    clubid = document.querySelector('input[name="clubname"]:checked').value

    fetch("/get_info?clubid="+clubid)
    .then((response) => response.text())
    .then((text) => {
    var info = text.split("`");

    // indices: name, mission, goals, mail, IG, YT, imlink, subbed

    // CLUB NAME
    document.getElementById("clubname").innerHTML = info[0];
    if (info[0] != "")
        document.getElementById("clubname").style.display = "inline-block";

    // CLUB MISSION
    document.getElementById("clubmission").innerHTML = info[1];
    if (info[1] != ""){
        document.getElementById("clubmission").style.display = "inline";
        document.getElementById("missiontd").style.display = "";
    }
    else{
        document.getElementById("missiontd").style.display = "none";
    }
    // CLUB GOALS
    document.getElementById("clubgoals").innerHTML = info[2];
    if (info[2] != "") {
        document.getElementById("clubgoals").style.display = "inline";
        const goalstr = document.getElementsByClassName("goals")[0];
        const goalstd = document.getElementsByClassName("goals")[1];
        goalstr.style.display = ""; 
        goalstd.style.display = ""; 
    }

    // CLUB EMAIL
    document.getElementById("clubemail").setAttribute('href', 'mailto:'+info[3]);
    if (info[3] != "")
        document.getElementById("clubemail").style.display = "inline";
    else
        document.getElementById("clubemail").style.display = "none";

    // CLUB INSTAGRAM
    document.getElementById("clubinstagram").setAttribute('href', info[4]);
    if (info[4] != "")
        document.getElementById("clubinstagram").style.display = "inline";
    else
        document.getElementById("clubinstagram").style.display = "none";

    // CLUB YOUTUBE
    document.getElementById("clubyoutube").setAttribute('href', info[5]);
    if (info[5] != "")
        document.getElementById("clubyoutube").style.display = "inline";
    else
        document.getElementById("clubyoutube").style.display = "none";

    // Socials TD
    if (info[3] == "" && info[4] == "" && info[5] == ""){
        document.getElementById("socialstd").style.display = "none";
    }
    else{
        document.getElementById("socialstd").style.display = "inline-block";
    }

    // CLUB IMLINK
    if (info[6] == "None")
        document.getElementById("clubimlink").src = 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Default_pfp.svg/1200px-Default_pfp.svg.png';
    else 
        document.getElementById("clubimlink").src = info[6];

    // GRAY BOX
    const namecard = document.getElementById("graynamecard");
    namecard.style.backgroundColor = "lightgrey";


    // CHECK SUBBED
    if (info[6] == "subscribed")
        document.getElementById('check').checked = true;
    else document.getElementById('check').checked = false;

    const previous = document.getElementsByClassName("search-results-card-selected");
    for (let i = 0; i < previous.length; i++) {
        previous[i].classList.remove('border', 'search-results-card-selected');
    }
    document.getElementById("card_"+clubid).classList.add('search-results-card-selected','border','border-warning','border-3');

    // make sub button appear
    document.getElementById("subbutton").style.display = "inline";
});
}

/*
function getTitle(id) {
    alert("TITLE")
    //document.getElementById("clubinfo").innerHTML = getInfo(selected_id)

    clubid = document.querySelector('input[name="clubname"]:checked').value
    // alert("selected element " + clubid)

    fetch("/get_info?clubid="+clubid)
    .then((response) => response.text())
    .then((text) => {
    var info = text.split("\n");
    });
    return info[1];
}
*/


function subscribeUser() {
    if (document.getElementById("check").checked) {
        fetch("/subscribe?clubid="+clubid+"&subscribe=1")
        .then((response) => response.text())
        .then((text) => {
            if (text=="success")
                alert("Successfully subscribed!")
            else alert("Error - unable to subscribe")
        });

        // add part with message about success

    }

    else {
        fetch("/subscribe?clubid="+clubid+"&subscribe=0")
        .then((response) => response.text())
        .then((text) => {
            if (text=="success")
                alert("Successfully unsubscribed!")
            else alert("Error - unable to unsubscribe")
        });

    }
}

