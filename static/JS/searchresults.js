//'use strict'

// https://stackoverflow.com/questions/9618504/how-to-get-the-selected-radio-button-s-value
//document.querySelector('input[name="clubname"]:checked').value;

function changeInfo() {

    clubid = document.querySelector('input[name="clubname"]:checked').value

    fetch("/get_info?clubid="+clubid)
    .then((response) => response.text())
    .then((text) => {
    var info = text.split("\n");

    document.getElementById("clubname").innerHTML = info[0];
    if (info[0] != "none")
        document.getElementById("clubname").style.display = "inline";
    document.getElementById("clubdesc").innerHTML = info[1];

    if (info[1] != "none")
        document.getElementById("clubdesc").style.display = "inline";
    document.getElementById("clubmeets").innerHTML = info[2];

    if(info[0] != "none" || info[1] != "none"){
        document.getElementById("namecard").style.backgroundColor = "gray";
    }
    if (info[2] != "none")
        document.getElementById("clubmeets").style.display = "inline";
    document.getElementById("clubcommit").innerHTML = info[3];

    if (info[3] != "none")
        document.getElementById("clubcommit").style.display = "inline";
    document.getElementById("clubwebsite").innerHTML = info[4];

    if (info[4] != "none")
        document.getElementById("clubwebsite").style.display = "inline";
    document.getElementById("clubverified").innerHTML = info[5];

    if (info[5] != "none")
        document.getElementById("clubverified").style.display = "inline";
    document.getElementById("clublastup").innerHTML = info[6];

    if (info[6] != "none")
        document.getElementById("clublastup").style.display = "inline";

    if (info[7] != "none")
        document.getElementById("clubimlink").src = info[7];

    else
        document.getElementById('clubimlink').src = "";


    if (info[8] == "subscribed")
        document.getElementById('check').checked = true;
    else document.getElementById('check').checked = false;

    const previous = document.getElementsByClassName("search-results-card-selected");
    for (let i = 0; i < previous.length; i++) {
        previous[i].classList.remove('border', 'search-results-card-selected');
    }
    document.getElementById("card_"+clubid).classList.add('search-results-card-selected','border','border-warning','border-3');
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

