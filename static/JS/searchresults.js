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
        alert("1")
    var info = text.split("\n")
    alert("2")
    document.getElementById("clubname").innerHTML = text[0]
    document.getElementById("clubdesc").innerHTML = text[1]
    document.getElementById("meets").innerHTML = text[2]
    document.getElementById("commitment").innerHTML = text[3]
    document.getElementById("website").innerHTML = text[4]
    document.getElementById("verified").innerHTML = text[5]
    document.getElementById("lastupdated").innerHTML = text[6]
    document.getElementById("imlink").innerHTML = text[7]});
}


