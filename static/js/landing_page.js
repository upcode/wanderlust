//
//min length of 8 char
//contains lowercase letter
//contains uppercase letter
//contains number special char
(function() {

}) ();
// set up vaiables to idetify different parts of the form
var password =
document.querySelector('.password');
var helperText = {  // password lengh has greater then 8
  charLength: document.querySelector ('.helper-text .length'),

  uppercase:
  document.querySelector('.helper-text .uppercase'),

  special:
  document.querySelector('.helper-text .special'),
};


//VALIDATION OBJECT

var pattern = {
    charLength: function() {
        if( password.value.length >= 8 ) {
            return true;
        }
    },

lowercase: function() {
  var regex = /^ (?=>*[a-z].+$/;
    if( regex.test(password.value) ) {
            return true;
        }

},
uppercase: function() {

}


// $(document).on("click", handler);



// $(document).ready(function(){
//    $('#myglobe').dialog({ autoOpen: false })
//    $('#').click(function(){ $('div.thedialog').dialog('open'); });
// });





