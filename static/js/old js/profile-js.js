function profileInfo(data){
    console.log(data);

    $('#first').html(data.first);

    $('#last').html(last);

    $('#username').html(username);

    $('#city').html(city);

    $('#state').html(state);

    $('#quote').html(quote);

    $('#about').html(about);
  }

function profile(evt) {
  evt.preventDefault();
  var first = $('#first').val();

  var last = $('#last').val();

  var username = $('#username').val();

  var quote = $('#quote').val();

  var city = $('#city').val();

  var state = $('#state').val();

  var about = $('#about').val();

  console.log("in profile");

  $.post('/profile', {'first':first,'last':last,'quote':quote,
 'city':city,'state':state,'about':about
  }, profileInfo);
}

$("#myForm").on('submit', profile);