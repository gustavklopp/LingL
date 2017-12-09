function ajax_uploaded_text(){
	/* called by text_detail.html:
	 upload a text file */
	var form = $("#uploaded_textform")
	var data_to_go = new FormData(form[0]);
	var token =  form.find('input[name=csrfmiddlewaretoken]').val(); // Indispensable. Get the csrf already defined in the form
	data_to_go.append('csrfmiddlewaretoken', token);
	$.ajax({
			url: '/uploaded_text/', 
			//dataType: 'json',
		    type: 'POST',
			cache: false,
			processData: false,
			contentType: false,
			data:  data_to_go,
			success: function(data){ 
				data = JSON.parse(data);
				if ('error' in data) {
					$('#uploaded_textform').find('.controls').append('<div class="text-danger">'+data['error']+'</div>');
				} else {
					$('#id_title').val(data['title']);
					$('#id_text').val(data['text']);
					}
				},
			error : function(data , status , xhr){ console.log('ERROR'); console.log(data); console.log(status); console.log(xhr); }
	});	
	return false;
}