(function(){  // get form element
    var form = document.getElementById('login');  // when user subits from
    addEvent(form, 'submit', function(e) {  //stop it from being sent
        e.preventDefault();
        var elements = this.elements; // get all the form elements
        var username = elements.username.value;  // select username entered
        var msg = 'Welcome' + username; //create welcom message
        document.getElementById('main').textContent = msg; //write welcome message
    });
}());