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


 function unsub_tag(tag) {
    fetch("/subscribe_tag?tag="+encodeURIComponent(tag)+"&subscribe_tag=0")
    .then((response) => response.text())
    .then((text) => {
       if (text=="success") {
          alert("Successfully unsubscribed from tag '" + tag + "'!")
       }
       else if (text=="success_isofficer") {
         alert("Successfully unsubscribed from tag '" + tag + "', except for clubs you are an officer of.")
      }
       else alert("Error - unable to unsubscribe from tag " + tag)
    })
    .then(() => {location.reload()});
}
