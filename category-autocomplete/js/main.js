$( document ).ready(function() {
  $('#ajax').on('input',function(e){
    $.ajax({
      url: "http://en.wikipedia.org/w/api.php",
      data: { action: 'query', list: 'allcategories', format: 'json', formatversion: '2', acprefix: $('#ajax').val()},
      dataType: 'jsonp',
      success: processResult
    });
  });
});

function processResult(apiResult){
  $('#json-datalist').html('');
  for (var i = 0; i < apiResult.query.allcategories.length; i++){
    item = apiResult.query.allcategories[i].category;
    // Create a new <option> element.
    var option = document.createElement('option');
    // Set the value using the item in the JSON array.
    option.value = item;
    // Add the <option> element to the <datalist>.
    $('#json-datalist').append(option);
  }
}
