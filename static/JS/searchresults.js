//'use strict'

// https://stackoverflow.com/questions/9618504/how-to-get-the-selected-radio-button-s-value
//document.querySelector('input[name="clubname"]:checked').value;

function changeInfo() {

    //document.getElementById("clubinfo").innerHTML = getInfo(selected_id)

    clubid = document.querySelector('input[name="clubname"]:checked').value
    // alert("selected element " + clubid)

    fetch("/get_info?clubid="+clubid)
    .then((response) => response.text())
    .then((text) => {
    var info = text.split("\n");
    document.getElementById("clubname").innerHTML = info[0];
    document.getElementById("clubdesc").innerHTML = info[1];
    document.getElementById("clubmeets").innerHTML = info[2];
    document.getElementById("clubcommit").innerHTML = info[3];
    document.getElementById("clubwebsite").innerHTML = info[4];
    document.getElementById("clubverified").innerHTML = info[5];
    document.getElementById("clublastup").innerHTML = info[6];
    document.getElementById("clubimlink").innerHTML = info[7];
    document.getElementById("clubimage").src = 'https://images.squarespace-cdn.com/content/v1/57b50c7559cc680955b06c27/1502749418326-AIJQ3QYSG9NOGDQ2DHRR/Full+horizontal+Logo+transparent.png?format=1500w';
});
}


