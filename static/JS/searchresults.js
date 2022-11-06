//'use strict'

// https://stackoverflow.com/questions/9618504/how-to-get-the-selected-radio-button-s-value
//document.querySelector('input[name="clubname"]:checked').value;

function changeInfo() {

    //document.getElementById("clubinfo").innerHTML = getInfo(selected_id)

    clubid = document.querySelector('input[name="clubname"]:checked').value
    // alert("selected element " + clubid)

    fetch("/get_info?clubid="+clubid)
    .then((response) => response.text())
    .then((text) => document.getElementById("clubinfo").innerHTML=text)
    .then((text) => document.getElementById("clubname").innerHTML=text[8]);
    //update_info(blob.arrayBuffer())
} 
/*
function changeInfo() {

    //document.getElementById("clubinfo").innerHTML = getInfo(selected_id)

    clubid = document.querySelector('input[name="clubname"]:checked').value
    // alert("selected element " + clubid)

    fetch("/get_info?clubid="+clubid)
    .then((response) => response.text())
    .then((text) => document.getElementById("clubinfo").innerHTML=text);
    //update_info(blob.arrayBuffer())

    fetch("/get_name?clubid="+clubid)
    .then((response) => response.text())
    .then((text) => document.getElementById("clubname").innerHTML=text);
    fetch("/get_desc?clubid="+clubid)
    .then((response) => response.text())
    .then((text) => document.getElementById("clubdesc").innerHTML=text);
    
    fetch("/get_meets?clubid="+clubid)
    .then((response) => response.text())
    .then((text) => document.getElementById("clubmeets").innerHTML=text);
    
    fetch("/get_commit?clubid="+clubid)
    .then((response) => response.text())
    .then((text) => document.getElementById("clubcommit").innerHTML=text);
    
    fetch("/get_website?clubid="+clubid)
    .then((response) => response.text())
    .then((text) => document.getElementById("clubwebsite").innerHTML=text);
    
    fetch("/get_verified?clubid="+clubid)
    .then((response) => response.text())
    .then((text) => document.getElementById("clubverified").innerHTML=text);/*
    fetch("/get_lastup?clubid="+clubid)
    .then((response) => response.text())
    .then((text) => document.getElementById("clublastup").innerHTML=text);
    fetch("/get_imlink?clubid="+clubid)
    .then((response) => response.text())
    .then((text) => document.getElementById("clubimlink").innerHTML=text);*/

function update_info() {
    document.getElementById("clubname").innerHTML = "hi"//blob[0].text()
    document.getElementById("clubdesc").innerHTML = blob[1].text()
    document.getElementById("meets").innerHTML = blob[2]
    document.getElementById("commitment").innerHTML = blob[3]
    document.getElementById("website").innerHTML = blob[4]
    document.getElementById("verified").innerHTML = blob[5]
    document.getElementById("lastupdated").innerHTML = blob[6]
    document.getElementById("imlink").innerHTML = blob[7]
}
