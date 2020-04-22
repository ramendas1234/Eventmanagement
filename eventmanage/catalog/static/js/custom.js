jQuery(document).ready(function($){
	//alert('i am loadded');
	$(document).on('click','.filter-by-category a',function(){
		catgid = $(this).data('catgid');
		text = $(this).text();
		$('#filterByCategoryButton').text(text);
		$('#filterCategory').val(catgid);
		$('#filterForm').submit();
	});

	$(document).on('submit','#filterForm',function(e){
		e.preventDefault();
		$('#event-list-inner').empty()
		var pathname = window.location.pathname; 
		url = pathname+'event-filter/' ;
		
		var formData = {
			'filterby_time': $('#filterTime').val(),
			'filterby_category': $('#filterCategory').val(),
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

	})

})