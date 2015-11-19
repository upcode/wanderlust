
    // sending to my server
// created functon called add adventure using ajax call to submit users new item on the list to be stored in the sever.
// function addAdventure passed in evt
//use a post method to route to sever which is form action="/adventurelist"
// in order to pass info have to pass ajax as dictionary
// pass fucntionn dta

// method prepares the request and has three prams
  // method get or post
  // route path
  // data  form is sending

function addAdventure(evt) {
  evt.preventDefault();
  var new_item = $('#itemDescription').val();

  $.post('/adventurelist', {'place':new_item}, function (data){
    console.log(data);
    $('#adventure-list').append("<li>"+ new_item +"</li>");

  });

}
$("#adventurelist").on('submit-button', addAdventure);
