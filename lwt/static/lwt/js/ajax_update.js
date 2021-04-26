/* update all parameters for the word, similar words of this word, compound words in HTML */
function update_data_of_wo_cowo_and_sims(data, op){
	// update parameters of the word/simword and the counter at the top
	$.each(data['wo_id_to_update_in_ajax'], function(idx, val){
			update_status(val, op, data['wostatus']);
			update_translation(val, op, data['wotranslation']);
			update_romanization(val, op, data['woromanization']);
			update_title(val, op, data['iscompoundword'], data['wowordtext'], 
								  data['wotranslation'], data['woromanization'], data['wostatus'],
								  data['cowotranslation'], data['coworomanization'], data['cowostatus'])
		});
	// compoundword:
	$.each(data['cowo_id_to_update_in_ajax'], function(idx, val){
			update_iscompoundword(val, op);
			update_show_compoundword(val, op);
			update_costatus(val, op, data['wostatus']);
			update_cotranslation(val, op, data['wotranslation']);
			update_coromanization(val, op, data['woromanization']);
			if (op == 'del'){ // the cowo in the cowo_id list, if with the op 'del' are evidently to be delete.
				data['iscompoundword'] = 'False';
			}
			update_title(val, op, data['iscompoundword'], data['wowordtext'], 
								  data['wotranslation'], data['woromanization'], data['wostatus'],
								  data['cowotranslation'], data['coworomanization'], data['cowostatus']);
		});
}

/* Helper functions for update_data_of_wo_cowo_and_sims() */

/* UPDATING THE STATUS (WELL-KNOWN or IGNORED) 
	called by: - helpage.js: shortcut keyboard when clicking on 'a' or 's'
			   - tooltip_link.js: the link inside the tooltip 
	@event	the event which has triggered the function
	@wo_id	the id of the word
	@status the updated status (number in string) of the word (for ex.: '101' for ignored) */
function ajax_update_status(event, wo_id, status) {
	$.ajax({url: '/termform/', 
			type: 'GET',
			dataType: 'json',
			data: 
				{ 
					'op':'update_status', 'status': status, 'wo_id' : wo_id,
				},
			success: function(data){ 
				// don't update the topright panel if the clicked word has already move to a next word
				var sel_word = $('.clicked');
				if (data['wowordtext'] == sel_word.attr('wowordtext')){
					$('#topright.text_read').html(data['html']); 
				}
				// update status of the word and the counter at the top
				$.each(data['wo_id_to_update_in_ajax'], function(idx, val){ // val=wo_id
						update_status(val, '', data['wostatus']);
						//update the title in word also
						update_title(val, '', data['iscompoundword'], data['wowordtext'], 
								  data['wotranslation'], data['woromanization'], data['wostatus'],
								  data['cowotranslation'], data['coworomanization'], data['cowostatus'])
						});
			},
			error : function(data , status , xhr){ console.log('ERROR');//error console.log(data); console.log(status); console.log(xhr);
			}
	});
}

/* UPDATING THE <SPAN> OF WORDS IN THE TEXT_READ --> I.E THE CLICKED TOOLTIP 
(the updating of the workcount is done here also) */
/* update status of the word in question: */
function update_status(wo_id, op, wostatus){
				if (op == 'del'){
						$('span[woid='+wo_id+']').attr('wostatus','0');}
				else {
						$('span[woid='+wo_id+']').attr('wostatus', wostatus);}

				var originalcolor =$('span[woid='+wo_id+']').css('background-color'); 
				$('span[woid='+wo_id+']').animate( // animation background-color thx to Jquery UI
						{backgroundColor: "#aa0000"}, 150, function(){
							$('span[woid='+wo_id+']').css('background-color', originalcolor);
							}
						);
				originalcolor = ''; // clean the variable
				// increment/decrement the number at the counter at the top
				update_workcount();
}

/* update the translation of the word in question: */
function update_translation(wo_id, op, wotranslation){
				$('span[woid='+wo_id+']').attr('wotranslation',wotranslation);
}

/* update the romanization of the word in question: */
function update_romanization(wo_id, op, woromanization){
				$('span[woid='+wo_id+']').attr('woromanization',woromanization);
}

// for compoundwords, same functions of updating:

/* update the parameter iscompoundword of the word in question:*/
function update_iscompoundword(wo_id, op){
				if (op == 'del'){
					$('span[woid='+wo_id+']').attr('isCompoundword','False');
				} else {
					$('span[woid='+wo_id+']').attr('isCompoundword','True');
				}
}

/* update the show_compoundword bool of the word in question:*/
function update_show_compoundword(wo_id, op){
				if (op == 'del'){
					$('span[woid='+wo_id+']').attr('show_compoundword','False');
				} else {
				$('span[woid='+wo_id+']').attr('show_compoundword','True');
				}
}

/* update status of the word in question:*/
function update_costatus(wo_id, op, wostatus){
				if (op == 'edit' || op == 'similar'){
						$('span[woid='+wo_id+']').attr('cowostatus', wostatus);}
				else if (op == 'del'){
						$('span[woid='+wo_id+']').attr('cowostatus','0');}
				else if (op == 'new'){
						$('span[woid='+wo_id+']').attr('cowostatus','1');}
				else if (op == 'wellkwn'){
						$('span[woid='+wo_id+']').attr('cowostatus','100');}
				else if (op == 'ignored'){
						$('span[woid='+wo_id+']').attr('cowostatus','101');}
				// increment/decrement the number at the counter at the top
				update_workcount();
}

/* update the translation of the word in question:*/
function update_cotranslation(wo_id, op, wotranslation){
	$('span[woid='+wo_id+']').attr('cowotranslation',wotranslation);
}

/* update the romanization of the word in question:*/
function update_coromanization(wo_id, op, woromanization){
	$('span[woid='+wo_id+']').attr('coworomanization',woromanization);
}

/* update the title */
function update_title(wo_id, op, iscompoundword, wowordtext, wotranslation, woromanization, wostatus, 
															 cowotranslation, coworomanization, cowostatus){
	var title = wowordtext;
	title += create_tooltip_title('word_symbol', wotranslation, woromanization, wostatus);
	if (iscompoundword == 'true' || iscompoundword == 'True' || iscompoundword == true){
		title += create_tooltip_title('coword_symbol', cowotranslation, coworomanization, cowostatus);
	}
	$('span[woid='+wo_id+']').attr('title', title);
}

/* called by update_status (for Cliked tooltip)
 change the number of word 'TO DO' at the top of text_read.html*/
function update_workcount(){
	var work_left_todo = $('span[woid][wostatus=0]').length - $('span[woid][iscompoundword="True"][cowostatus!=0]').length;
	$('#word_left_todo').html('&nbsp;'+work_left_todo.toString()+'&nbsp;');
	// and change the color if necessary:
	if (work_left_todo == 0){
		$('#word_left_todo').attr('wostatus','1'); 
		// and disable the 'i know all' button
		$('button#iknowall').attr('disabled','');
	} else {
		$('#word_left_todo').attr('wostatus','0'); }
}

/* NOT USED FINALLY */
/* update span attribute of word in text_read */
/*
function ajax_update_HTML_show_compoundword(compoundword_id_list, show_compoundword){
	$.each(compoundword_id_list, function(key, val){
		$('span[woid='+val+']').attr('show_compoundword', show_compoundword);
	});
}*/

/* NOT USED finally */
/* called by: click_ctrlclick_toggle() */
/*
function ajax_update_DB_show_compoundword(wo_id, show_compoundword){
	$.ajax({url: '/update_show_compoundword/', 
			type: 'GET',
			dataType: 'json',
			data: {
					'wo_id' : wo_id, 
					'show_compoundword' : show_compoundword,
					},
			success: function(data){ 
				ajax_update_HTML_show_compoundword(data['compoundword_id_list'], show_compoundword);
			},
			 error : function(data , status , xhr){ console.log(data); console.log(status); console.log(xhr);}
			});
} */