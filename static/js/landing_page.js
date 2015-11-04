// //Js to open modal windown from form
// var formErrors = {% if form_errors %}true{% else %}false{% endif %};
// $(document).ready(function(){
//     if (formErrors) {
//         $('.modal').modal('show');
//     }
// });

// $('#myModal').on('shown.bs.modal', function () {
//   $('#myInput').focus()
// })




//Jquery for modal
    //$(#myglobe:hidden).onclick(function(){
        //show

//     }; function()
//     //onhide
// });



    $(document).click(function(){
        alert("Hello")
    });

    $("#myglobe").click(function(e))
    e.stopPropagation();
    return false;

});

var handler = function(event){
  // if the target is a descendent of container do nothing
  if($(event.target).is(".container, .container *")) return;

  // remove event handler from document
  $(document).off("click", handler);

  // dostuff
}

$(document).on("click", handler);



$(document).ready(function(){
   $('#myglobe').dialog({ autoOpen: false })
   $('#').click(function(){ $('div.thedialog').dialog('open'); });
});





// MODAL WINDOW PASSWORD
$(function(){
  $('#loginform').submit(function(e){
    return false;
  });
$('#modaltrigger').leanModal({ top: 110, overlay: 0.45, closeButton: ".hidemodal" });
});