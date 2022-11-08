//'use strict'

// https://stackoverflow.com/questions/9618504/how-to-get-the-selected-radio-button-s-value
//document.querySelector('input[name="clubname"]:checked').value;

function changeInfo(id) {

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
    document.getElementById("clubimage").src = 'https://i0.wp.com/statisticsbyjim.com/wp-content/uploads/2020/09/association-152746_640.png?resize=300%2C300&ssl=1';

    const previous = document.getElementsByClassName("search-results-card-selected");
    for (let i = 0; i < previous.length; i++){
        previous[i].classList.remove('border', 'search-results-card-selected');
    }
    document.getElementById("card_"+clubid).classList.add('search-results-card-selected','border','border-warning','border-3');
});
}

function getTitle(id) {

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


