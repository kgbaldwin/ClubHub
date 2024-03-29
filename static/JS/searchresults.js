//'use strict'

// https://stackoverflow.com/questions/9618504/how-to-get-the-selected-radio-button-s-value
//document.querySelector('input[name="clubname"]:checked').value;

function changeInfo() {

    clubid = document.querySelector('input[name="clubname"]:checked').value

    fetch("/get_info?clubid="+clubid)
    .then((response) => response.text())
    .then((text) => {
    console.log(text)
    var info = text.split("`");
    console.log(info)

    // make initial message disappear
    document.getElementById('none-selected').style.display='none';

    // indices: name, mission, goals, mail, IG, YT, imlink, subbed

    // CLUB NAME
    document.getElementById("clubname").innerHTML = info[0];
    if (info[0] != "")
        document.getElementById("clubname").style.display = "inline-block";

    // CLUB MISSION
    document.getElementById("clubmission").innerHTML = info[1];
    const missioncard = document.getElementById("missioncard");
    const clubmission = document.getElementById('clubmission');
    const missionbr = document.getElementById("missionbr");
    if (info[1] != ""){
        missioncard.style.display ="";
        clubmission.style.display="";
        missionbr.style.display="";
    }
    else{
        missioncard.style.display = "none";
        clubmission.style.display="none";
        missionbr.style.display="none";
    }
    // CLUB GOALS
    document.getElementById("clubgoals").innerHTML = info[2];
    const goalscard = document.getElementById("goalscard");
    const clubgoals = document.getElementById("clubgoals");
    const goalsbr = document.getElementById("goalsbr");
    if (info[2] != "") {
        goalscard.style.display="";
        clubgoals.style.display="";
        goalsbr.style.display="";
    }
    else{
        goalscard.style.display="none";
        clubgoals.style.display="none";
        missionbr.style.display="none";
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

    // Get club tags
        document.getElementById("tagsdiv").style.display="inline-block";
        const tagscard = document.getElementsByClassName("tagscard")[0];
        tagscard.style.backgroundColor = 'lightgrey';
        tagscard.style.display="inline-block";
        const tags = info[7].split('#');
        var stringBuilder = "";
        for (let i = 0; i < tags.length - 1; i++){
            stringBuilder += tags[i];
            if (tags.length - i > 2) {
                stringBuilder += ", ";
            }
        }
        document.getElementById("tagsdiv").innerHTML = stringBuilder;

    // CHECK SUBBED

    // make sub button appear
    document.getElementById("subbutton").style.display = "inline";
    if (info[8] == "subscribed"){
        const checkSub = document.getElementsByClassName('checkSub');
        checkSub[1].style.display = "none";
        const checkUnSub = document.getElementsByClassName('checkUnSub');
        checkUnSub[0].style.display = "inline-block";
        document.getElementById('check').checked = true;
    }
    else {
        const checkSub = document.getElementsByClassName('checkSub');
        checkSub[1].style.display = "inline-block";
        const checkUnSub = document.getElementsByClassName('checkUnSub');
        checkUnSub[0].style.display = "none";
        document.getElementById('check').checked = false;
    }
    const previous = document.getElementsByClassName("search-results-card-selected");
    for (let i = 0; i < previous.length; i++) {
        previous[i].classList.remove('border', 'search-results-card-selected');
    }
    document.getElementById("card_"+clubid).classList.add('search-results-card-selected');

});
}

function loadAnnouncements() {

    fetch("/get_club_announcements?clubid="+clubid)
        .then((response) => response.text())
        .then((text) => {

            if (text !== 'announcements error') {


                var ann_array = text.split("`");
                const ann_div = document.getElementById("club-announcements");
                var htmlBuilder = "";

                let announcements = [];
                let timestamps = [];
                let dates = [];
                let netids = [];
                let j = 0;
                for (let i = 0; i < ann_array.length-1;i++){ //last index is bloat
                    if(i % 3 == 0){
                        announcements[j] = ann_array[i];
                    }
                    else if ((i - 1) % 3 == 0){
                        timestamps[j] = ann_array[i];
                        dateandtime = ann_array[i].split(",");
                        dates[j] = dateandtime[0];
                    }
                    else{
                        netids[j] = ann_array[i];
                        j++;
                    }
                }

                for (let i = 0; i < announcements.length; i++){
                    htmlBuilder += `<div class="ann-card">`
                    htmlBuilder += `<div style="color:white;">${netids[i]}`
                    htmlBuilder += `<small style="color:#ececec;"> ${dates[i]}</small>:</div>`
                    htmlBuilder += `<div style="font-size:1.4rem;">${announcements[i]}</div></div><br>`
                    //if (announcements.length - i > 1)
                    //  htmlBuilder += '<br>';
                }

                ann_div.innerHTML = htmlBuilder;

                /*for (let i = 0; i < ann_array.length; i++){
                    htmlBuilder += ann_array[i]
                    if (ann_array.length - i > 1)
                        htmlBuilder += '<br>'
                }
                ann_div.innerHTML = htmlBuilder;*/
                const ann_body = document.getElementsByClassName("announcements-body");
                if (ann_array.length > 1){
                    ann_body[0].style.display = "inline-block";
                    ann_body[0].style.backgroundColor = "lightgrey";
                }
                else {
                    ann_body[0].style.display = "none";
                }
            }
        });
}


function subscribeUser() {
    if (document.getElementById("check").checked) {
        fetch("/subscribe?clubid="+clubid+"&subscribe=1")
        .then((response) => response.text())
        .then((text) => {
            if (text=="success"){
                alert("Successfully subscribed!")
                const checkSub = document.getElementsByClassName('checkSub');
                checkSub[1].style.display = "none";
                const checkUnSub = document.getElementsByClassName('checkUnSub');
                checkUnSub[0].style.display = "inline-block";
            }
            else alert(text)
        });
    }

    else {
        fetch("/subscribe?clubid="+clubid+"&subscribe=0")
        .then((response) => response.text())
        .then((text) => {
            if (text=="cannot unsubscribe officer"){
                document.getElementById("check").checked = true
                alert("Cannot unsubscribe officer from club")
            }
            else if (text=="success"){
                alert("Successfully unsubscribed!")
                const checkSub = document.getElementsByClassName('checkSub');
                checkSub[1].style.display = "inline-block";
                const checkUnSub = document.getElementsByClassName('checkUnSub');
                checkUnSub[0].style.display = "none";
            }
            else alert("Error - unable to unsubscribe")
        });

    }
}

