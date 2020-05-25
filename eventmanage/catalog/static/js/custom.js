jQuery(document).ready(function($){
//alert('i am loadded');
// date wise filter
$(document).on('click','.filter-by-time a',function(){
date = $(this).data('value');
text = $(this).text();
$('#filterByTimeButton').text(text);
$('#filterTime').val(date);
$('#filterForm').submit();
});
// Category wise filter
$(document).on('click','.filter-by-category a',function(){
catgid = $(this).data('catgid');
text = $(this).text();
$('#filterByCategoryButton').text(text);
$('#filterCategory').val(catgid);
$('#filterForm').submit();
});
// Listing type wise filter
$(document).on('click','.listing-type a',function(){
listing_type = $(this).data('value');
text = $(this).text();
$('#listingButton').text(text);
$('#filterListingType').val(listing_type);
$('#filterForm').submit();
});
$(document).on('submit','#filterForm',function(e){
e.preventDefault();
$('#event-list-inner').empty()
var pathname = window.location.pathname;
var action = $(this).attr('action');
url = pathname+action ;

var formData = {
'filterby_time': $('#filterTime').val(),
'filterby_category': $('#filterCategory').val(),
'listing_type': $('#filterListingType').val(),
'sort_by': $('#sortBy').val(),
'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
}
$.ajax({
type:'POST',
url:url,
data:formData,
encode : true
}).done(function(response){
$('#event-list-inner').html(response)
});
});
$(document).on('submit','#update_profile',function(e){
e.preventDefault();
var formData = {
'first_name': $('#first_name').val(),
'last_name': $('#last_name').val(),
'username': $('#username').val(),
'email': $('#email').val(),
'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
}
$.ajax({
type: 'POST',
'url': '/profile/update',
data: formData,
encode: true
}).done(function(response){
response = JSON.parse(response);
if(response.flag){
swal("Success!", response.msg, "success")
}else{
swal("Oops", response.msg, "error")
}
});
});


$(document).on('change','#id_profile_image',function(e){
$('.profile-image-loader').show();
setTimeout(function(){ $('#changeDp').submit() }, 3000);

});

/*
$(document).on('submit','#changeDpg',function(e){
	e.preventDefault();
	var formData = new FormData();


var fileInput = document.getElementById('id_profile_image');
var file = fileInput.files[0];
formData.append('image', file);
formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());

$.ajax({
url: '/abc/',
type: 'POST',
data: formData,
processData: false,
contentType: false,
success: function(data) {
alert('success');
}
});

});  */




})