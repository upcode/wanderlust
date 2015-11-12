$(function() {
  $('ul').before('<p class="notice">Just updated</p>');
  $('li.hot').prepend('+ ');
  var $newListItem = $('<li><em>Place</em>event</li>');
  $('li:last').after($newListItem);
});

$(function() {
    $('button').click(function() {
        var adventure_item = $('#addAdventure').val();
        $.ajax({
            url: '/list2',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});