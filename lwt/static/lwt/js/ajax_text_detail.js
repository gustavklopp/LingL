function ajax_uploaded_text(op){
	/* called by text_detail.html:
	 upload a text file */
	if (op == 'uploaded_text'){
		var form = $("#uploaded_textform")
	} else if (op == 'uploaded_pdf'){
		var form = $("#uploaded_pdfform")
	}
	var data_to_go = new FormData(form[0]);
	var token =  form.find('input[name=csrfmiddlewaretoken]').val(); // Indispensable. Get the csrf already defined in the form
	data_to_go.append('csrfmiddlewaretoken', token);
	data_to_go.append('op', op);
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
					var title = data['title'].replace(/_/g, ' ');
					$('#id_title').val(title);
					if (op == 'uploaded_text'){
						$('#id_text').val(data['text']);
					    }
					}
				},
			error : function(data , status , xhr){ console.log('ERROR'); console.log(data); console.log(status); console.log(xhr); }
	});	
	return false;
}

$(document).ready(function(e) {
	/* clicking on the radio button in termform to choose link */
	$('#uploaded_textform input#id_uploaded_text').change(function() {
			$("#uploaded_textform").submit(ajax_uploaded_text('uploaded_text'));
					});
	$('#uploaded_pdfform input#id_uploaded_text').change(function() {
			$("#uploaded_pdfform").submit(ajax_uploaded_text('uploaded_pdf'));
					});
});
					
					
					