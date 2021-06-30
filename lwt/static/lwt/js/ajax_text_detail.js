/* called by text_detail.html:
 upload a text file or a document 
	@op 'uploaded_doc' or 'uploaded_text '*/
function ajax_uploaded_text(op){
	if (op == 'uploaded_text'){
		var form = $("#uploaded_textform")
	} else if (op == 'uploaded_doc'){
		var form = $("#uploaded_docform")
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
					// the file_id will be used when submitting the form to get the pathname of the file later
					$('form.text_detail').append('<input name="file_id" id="file_id" value='+data['file_id']+' hidden>');
					$('form.text_detail').parent().removeClass('disabled_form');
				}
			},
			error : function(data , status , xhr){ console.log('ERROR'); console.log(data); console.log(status); console.log(xhr); }
	});	
	return false;
}

function display_loading_popup(){
	// all the background is disabled:
	$('<div></div>').appendTo('body').css({
		  'position': 'fixed',
		  'padding': '0',
		  'margin': '0',
		  'top': '0',
		  'left': '0',
		  'width': '100%',
		  'height': '100%',
		  'opacity': '0.5',
		  'background-color': 'black',
		  'z-index': '100',
	});
	// display the popup
	$('#loadingpopup').prop('hidden', false)
	.dialog({
		modal: true,
		zIndex: '101 !important', autoOpen: true,
		width: 'auto', resizable: false,
	   // position: {my: "center",  at: "center", of: $("body"),within: $("body") }
        open: function(event, ui) { 
            //hide titlebar.
            $(this).parent().children('.ui-dialog-titlebar').remove();
        },
	}).css('background-color', 'white'); // end of '.dialog({'

}
$(document).ready(function(e) {
	/* clicking on the radio button in termform to choose link */
	$('#uploaded_textform input#id_uploaded_text').change(function() {
			$("#uploaded_textform").submit(ajax_uploaded_text('uploaded_text'));
					});
	$('#uploaded_docform input#id_uploaded_text').change(function() {
			$("#uploaded_docform").submit(ajax_uploaded_text('uploaded_doc'));
					});

	// display a loading popup after saving
	$('#submit-id-save').bind('click', display_loading_popup);
	$('#submit-id-save_read').bind('click', display_loading_popup);
});
					
					
					