function unsubscribe(input) {

    fetch("/subscribe?subscribe=0&clubid="+input)
    .then((response) => response.text())
    .then((text) => {
       if (text=="cannot unsubscribe officer"){
         alert("Cannot unsubscribe officer from club")
       }
       else if (text=="error"){
         alert(text)
       }
    })
    .then(() => {location.reload();})

}

function sub_tag(tag) {
   document.getElementById("sub-loading").style.display="inline";
   fetch("/subscribe_tag?tag="+encodeURIComponent(tag)+"&subscribe_tag=1")
   .then((response) => response.text())
   .then((text) => {
      if (text=="success"){
         document.getElementById("sub-loading").style.display="none";
         alert("Successfully subscribed to tag " + tag + "!");
      }
      else {
         document.getElementById("sub-loading").style.display="none";
         alert("Error - unable to subscribe to tag " + tag)
      }
   })
   .then(() => {location.reload()});
}


function unsub_tag(tag) {
   document.getElementById("unsub-loading").style.display="inline";
    fetch("/subscribe_tag?tag="+encodeURIComponent(tag)+"&subscribe_tag=0")
    .then((response) => response.text())
    .then((text) => {
       if (text=="success") {
         document.getElementById("unsub-loading").style.display="none";
         alert("Successfully unsubscribed from tag '" + tag + "'!")
       }
       else if (text=="success_isofficer") {
         document.getElementById("unsub-loading").style.display="none";
         alert("Successfully unsubscribed from tag '" + tag + "', except for clubs you are an officer of.")
      }
       else {
         document.getElementById("unsub-loading").style.display="none";
         alert("Error - unable to unsubscribe from tag " + tag)
      }
    })
    .then(() => {location.reload()});
}

function toggle(tag) {
   checkbox = document.getElementById(tag);
   checkbox.checked = !checkbox.checked;
   const findInd = (element) => element == tag;
   if (checkbox.checked){
      tags_tf[tags_selection.findIndex(findInd)] = true;
   }
   else{
      tags_tf[tags_selection.findIndex(findInd)] = false;
   }
   let htmlBuilder = "";
   selected_tags = get_selected_tags();
   for (let i = 0; i < selected_tags.length; i++){
      htmlBuilder += selected_tags[i];
      if (selected_tags.length - i > 1)
         htmlBuilder += ', ';
   }
   document.getElementById('selected_tags').innerHTML = htmlBuilder;
}

function get_selected_tags(){
   let selected_tags = [];
   // append all selected tags
   for (let i = 0; i < tags_selection.length; i++){
      if (tags_tf[i]) {
         selected_tags.push(tags_selection[i]);
      }
   }
   return selected_tags
}

