/* Functions inside the tooltip */

// CREATING A NEW WORD:  sends by AJAX data to refresh the top right of text_read with the form termform
// or EDITING A WORD:
/* called by: text_read_clickevent, if status == 0: op: 'new'
		and: create_link_newword: op: 'new'
		and: create_link_editword: op: 'edit' */
function tooltip_ajax_termform(wo_id, op, show_compoundword, compoundword_id_list, rtl) {
	if (show_compoundword){
		$.ajax({url: '/termform/', type: 'GET',
				data: {'op':op, 'compoundword_id_list': compoundword_id_list},
				success: function(data){
					var data = JSON.parse(data);
					$('#topright.text_read').html(data['html']);
					// and display the possible similar words:
					var r = _display_possiblesimilarword(data, wo_id);
					$('#result_possiblesimilarword').html(r);
				},
				 error : function(data , status , xhr){
						console.log(data); console.log(status); console.log(xhr);}
				});
	} else {
		$.ajax({url: '/termform/', type: 'GET',
				data: {'op':op, 'wo_id': wo_id},
				success: function(data){
					var data = JSON.parse(data);
					$('#topright.text_read').html(data['html']);
					// and display the possible similar words:
					var r = _display_possiblesimilarword(data, wo_id);
					$('#result_possiblesimilarword').html(r);
				},
				 error : function(data , status , xhr){
						console.log(data); console.log(status); console.log(xhr);}
				});
	}
}

/* delete a word and the similar words and compoundword with it */
function tooltip_ajax_del_word(wo_id) {
	$.ajax({url: '/termform/', 
			type: 'GET',
			dataType: 'json',
			data: 
				{ 
					'op':'del', 'wo_id' : wo_id,
				},
			success: function(data){ 
				$('#topright.text_read').html(data['html']); 
				update_data_of_wo_cowo_and_sims(data, 'del');
			},
			error : function(data , status , xhr){ console.log('ERROR');//error console.log(data); console.log(status); console.log(xhr);
			}
	});
}

/* same as above but we delete only one single word, not the similar words with it */
function tooltip_ajax_del_singleword(wo_id) {
	$.ajax({url: '/termform/', 
			type: 'GET',
			dataType: 'json',
			data: 
				{ 
					'op':'del', 'wo_id' : wo_id, 'singleword': true,
				},
			success: function(data){ 
				$('#topright.text_read').html(data['html']); 
				// update status of the word and the counter at the top
				update_status(wo_id, 'del');
				$('span[woid='+wo_id+']').attr('title', create_tooltip_title('▶',data['wowordtext'],'','','0'));
			},
			error : function(data , status , xhr){ console.log('ERROR');//error console.log(data); console.log(status); console.log(xhr);
			}
	});
}
