function ajax_update_word_simword_compoundword(data, op){
	/* update all parameters for the word, similar words of this word, compound words in HTML */
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

/* Helper functions for ajax_update_word_simword_compoundword() */

/* UPDATING THE STATUS (WELL-KNOWN or IGNORED) */
function ajax_update_status(wo_id, status) {
	$.ajax({url: '/termform/', 
			type: 'GET',
			dataType: 'json',
			data: 
				{ 
					'op':'update_status', 'status': status, 'wo_id' : wo_id,
				},
			success: function(data){ 
				$('#topright.text_read').html(data['html']); 
				// update status of the word and the counter at the top
				$.each(data['wo_id_to_update_in_ajax'], function(idx, val){
						update_status(val, status, '');
						update_title(val, op, data['iscompoundword'], data['wowordtext'], 
											  data['wotranslation'], data['woromanization'], data['wostatus'],
											  data['cowotranslation'], data['coworomanization'], data['cowostatus']);
					});
			},
			error : function(data , status , xhr){ console.log('ERROR');//error console.log(data); console.log(status); console.log(xhr);
			}
	});
}

/* UPDATING THE <SPAN> OF WORDS IN THE TEXT_READ --> I.E THE CLICKED TOOLTIP (the updating of the workcount is done here also) */
function update_status(wo_id, op, wostatus){
				/* update status of the word in question: */
				if (op == 'edit'){
						$('span[woid='+wo_id+']').attr('wostatus', wostatus);}
				else if (op == 'del'){
						$('span[woid='+wo_id+']').attr('wostatus','0');}
				else if (op == 'new'){
						$('span[woid='+wo_id+']').attr('wostatus','1');}
				else if (op == 'wellkwn'){
						$('span[woid='+wo_id+']').attr('wostatus','100');}
				else if (op == 'ignored'){
						$('span[woid='+wo_id+']').attr('wostatus','101');}
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

function update_translation(wo_id, op, wotranslation){
				/* update the translation of the word in question:*/
				$('span[woid='+wo_id+']').attr('wotranslation',wotranslation);
}

function update_romanization(wo_id, op, woromanization){
				/* update the romanization of the word in question: */
				$('span[woid='+wo_id+']').attr('woromanization',woromanization);
}

// for compoundwords, same functions of updating:
function update_iscompoundword(wo_id, op){
				/* update the parameter iscompoundword of the word in question:*/
				if (op == 'del'){
					$('span[woid='+wo_id+']').attr('isCompoundword','False');
				} else {
					$('span[woid='+wo_id+']').attr('isCompoundword','True');
				}
}

function update_show_compoundword(wo_id, op){
				/* update the show_compoundword bool of the word in question:*/
				if (op == 'del'){
					$('span[woid='+wo_id+']').attr('show_compoundword','False');
				} else {
				$('span[woid='+wo_id+']').attr('show_compoundword','True');
				}
}

function update_costatus(wo_id, op, wostatus){
				/* update status of the word in question:*/
				if (op == 'edit'){
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

function update_cotranslation(wo_id, op, wotranslation){
	/* update the translation of the word in question:*/
	$('span[woid='+wo_id+']').attr('cowotranslation',wotranslation);
}

function update_coromanization(wo_id, op, woromanization){
	/* update the romanization of the word in question:*/
	$('span[woid='+wo_id+']').attr('coworomanization',woromanization);
}

function update_title(wo_id, op, iscompoundword, wowordtext, wotranslation, woromanization, wostatus, 
															 cowotranslation, coworomanization, cowostatus){
	/* update the title */
	var title = wowordtext;
	title += create_tooltip_title('word_symbol', wotranslation, woromanization, wostatus);
	if (iscompoundword == 'true' || iscompoundword == 'True' || iscompoundword == true){
		title += create_tooltip_title('coword_symbol', cowotranslation, coworomanization, cowostatus);
	}
	$('span[woid='+wo_id+']').attr('title', title);
}

function update_workcount(){
	/* called by update_status (for Cliked tooltip)
	 change the number of word 'TO DO' at the top of text_read.html*/
	var work_left_todo = $('span[woid][wostatus=0]').length - $('span[woid][iscompoundword="True"][cowostatus!=0]').length;
	$('#word_left_todo').html('&nbsp;'+work_left_todo.toString()+'&nbsp;');
	// and change the color if necessary:
	if (work_left_todo == 0){
		$('#word_left_todo').attr('wostatus','1'); }
	else {
		$('#word_left_todo').attr('wostatus','0'); }
}

function ajax_update_HTML_show_compoundword(compoundword_id_list, show_compoundword){
	/* update span attribute of word in text_read */
	$.each(compoundword_id_list, function(key, val){
		$('span[woid='+val+']').attr('show_compoundword', show_compoundword);
	});
}

function ajax_update_DB_show_compoundword(wo_id, show_compoundword){
	/* called by: click_ctrlclick_toggle() */
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
}