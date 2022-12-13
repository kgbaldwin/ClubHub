
document.getElementById("tagdropdown").addEventListener('click',
    function (event) {
        event.stopPropagation();
    }
);


function toggle(tag) {
    checkbox = document.getElementById(tag);
    checkbox.checked = !checkbox.checked;

    update_selected()

}


function update_selected() {
    let htmlBuilder = "";
    let selected_tags = $('#tagdropdown input:checked');

    if (selected_tags.length > 0) {
        htmlBuilder += "Selected: "
    }

    for (let i = 0; i < selected_tags.length; i++) {
        htmlBuilder += selected_tags[i].value;
        if (i < selected_tags.length - 1) {
            htmlBuilder += ", "
        }
    }

    document.getElementById('selected_tags').innerHTML = htmlBuilder;

}

