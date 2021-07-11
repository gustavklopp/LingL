/* update all parameters for the word, similar words of this word, compound words in HTML */
function update_data_of_wo_cowo_and_sims(data, op){
	// update parameters of the word/simword and the counter at the top
	$.each(data['wo_id_to_update_in_ajax'], function(idx, val){
			// specific to words
			update_status(val, op, data['wostatus']);
			update_translation(val, op, data['wotranslation']);
			update_romanization(val, op, data['woromanization']);

			update_title(val,  data['iscompoundword'], data['wowordtext'], 
					   data['wotranslation'], data['woromanization'], data['wostatus'],
					   data['cowordtext'], data['cowotranslation'], data['coworomanization'], data['cowostatus'],
					   data['show_compoundword']);
		});
	// compoundword:
	$.each(data['cowo_id_to_update_in_ajax'], function(idx, val){
			// specific to compound words
			update_iscompoundword(val, op);
			update_show_compoundword(val, op);
			update_cowordtext(val, data['cowordtext']);
			// NOT USED finally... I've decided that 'costatus' is the same as ''status'.
//			update_costatus(val, op, data['cowostatus']);
			update_status(val, op, data['cowostatus']);

			update_cotranslation(val, op, data['cowotranslation']);
			update_coromanization(val, op, data['coworomanization']);
			if (op == 'del'){ // the cowo in the cowo_id list, if with the op 'del' are evidently to be delete.
				data['iscompoundword'] = 'False';
			}

			update_title(val, data['iscompoundword'], data['wowordtext'], 
						data['wotranslation'], data['woromanization'], data['wostatus'],
						data['cowordtext'], data['cowotranslation'], data['coworomanization'], data['cowostatus'],
						data['show_compoundword']);
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
	var DOCUMENT = window.DOCUMENT;
	$.ajax({url: '/termform/', 
			type: 'GET',
			dataType: 'json',
			data: 
				{ 
					'op':'update_status', 'status': status, 'wo_id' : wo_id,
				},
			success: function(data){ 
				// don't update the topright panel if the clicked word has already move to a next word
				var sel_word = DOCUMENT.find('.clicked');
				if (data['wowordtext'] == sel_word.attr('wowordtext')){
					$('#topright.text_read').html(data['html']); 
				}
				// update status of the word and the counter at the top
				$.each(data['wo_id_to_update_in_ajax'], function(idx, val){ // val=wo_id
						update_status(val, '', data['wostatus']);
						//update the title in word also
						update_title(val, data['iscompoundword'], 
					   	  data['wowordtext'], data['wotranslation'], data['woromanization'], data['wostatus'],
						  data['cowordtext'], data['cowotranslation'], data['coworomanization'], data['cowostatus'],
						  data['show_compoundword'])
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
	var DOCUMENT = window.DOCUMENT;
	if (op == 'del'){
			DOCUMENT.find('span[woid='+wo_id+']').attr('wostatus','0');}
	else {
			DOCUMENT.find('span[woid='+wo_id+']').attr('wostatus', wostatus);}

	var originalcolor = DOCUMENT.find('span[woid='+wo_id+']').css('background-color'); 
	DOCUMENT.find('span[woid='+wo_id+']').animate( // animation background-color thx to Jquery UI
			{backgroundColor: "#aa0000"}, 150, function(){
				DOCUMENT.find('span[woid='+wo_id+']').css('background-color', originalcolor);
				}
			);
	originalcolor = ''; // clean the variable
	// increment/decrement the number at the counter at the top
	update_workcount();
}

/* update the translation of the word in question: */
function update_translation(wo_id, op, wotranslation){
	var DOCUMENT = window.DOCUMENT;
	DOCUMENT.find('span[woid='+wo_id+']').attr('wotranslation',wotranslation);
}

/* update the romanization of the word in question: */
function update_romanization(wo_id, op, woromanization){
	var DOCUMENT = window.DOCUMENT;
	DOCUMENT.find('span[woid='+wo_id+']').attr('woromanization',woromanization);
}

// for compoundwords, same functions of updating:

/* update the parameter iscompoundword of the word in question:*/
function update_iscompoundword(wo_id, op){
	var DOCUMENT = window.DOCUMENT;
	if (op == 'del'){
		DOCUMENT.find('span[woid='+wo_id+']').attr('isCompoundword','False');
	} else {
		DOCUMENT.find('span[woid='+wo_id+']').attr('isCompoundword','True');
	}
}

/* update the show_compoundword bool of the word in question:*/
function update_show_compoundword(wo_id, op){
	var DOCUMENT = window.DOCUMENT;
	if (op == 'del'){
		DOCUMENT.find('span[woid='+wo_id+']').attr('show_compoundword','False');
	} else {
	DOCUMENT.find('span[woid='+wo_id+']').attr('show_compoundword','True');
	}
}

/* update cowordtext of the word in question:*/
function update_cowordtext(wo_id, cowordtext){
	var DOCUMENT = window.DOCUMENT;
	DOCUMENT.find('span[woid='+wo_id+']').attr('cowordtext', cowordtext);
}

// NOT USED finally... I've decided that 'costatus' is the same as ''status'.
/* update status of the word in question:*/
function update_costatus(wo_id, op, wostatus){
	var DOCUMENT = window.DOCUMENT;
	if (op == 'edit' || op == 'similar'){
			DOCUMENT.find('span[woid='+wo_id+']').attr('cowostatus', wostatus);}
	else if (op == 'del'){
			DOCUMENT.find('span[woid='+wo_id+']').attr('cowostatus','0');}
	else if (op == 'new'){
			DOCUMENT.find('span[woid='+wo_id+']').attr('cowostatus','1');}
	else if (op == 'wellkwn'){
			DOCUMENT.find('span[woid='+wo_id+']').attr('cowostatus','100');}
	else if (op == 'ignored'){
			DOCUMENT.find('span[woid='+wo_id+']').attr('cowostatus','101');}
	// increment/decrement the number at the counter at the top
	update_workcount();
}

/* update the translation of the word in question:*/
function update_cotranslation(wo_id, op, wotranslation){
	var DOCUMENT = window.DOCUMENT;
	DOCUMENT.find('span[woid='+wo_id+']').attr('cowotranslation',wotranslation);
}

/* update the romanization of the word in question:*/
function update_coromanization(wo_id, op, woromanization){
	var DOCUMENT = window.DOCUMENT;
	DOCUMENT.find('span[woid='+wo_id+']').attr('coworomanization',woromanization);
}

/* the Python True is not recognized as 'true' by Javascript */

function _is_true(variable){
	if (variable == 'True' || variable == 'true' || variable == true){
		return true
	} else {
		return false
	}
}
/* update the title */
function update_title(this_OR_wo_id, iscompoundword, wowordtext, wotranslation, woromanization, wostatus, 
						cowordtext, cowotranslation, coworomanization, cowostatus, show_compoundword){
	var DOCUMENT = window.DOCUMENT;
	var wo_title = wowordtext;
	var co_title = cowordtext;
	if (!(this_OR_wo_id instanceof jQuery)){
		var $this = DOCUMENT.find('span[woid='+this_OR_wo_id+']')	
	} else {
		var $this = this_OR_wo_id;
	}
	wo_title += create_tooltip_title('word_symbol', wotranslation, woromanization, wostatus);
	if (_is_true(iscompoundword)){
		co_title += create_tooltip_title('coword_symbol', cowotranslation, coworomanization, cowostatus);
	}
	if (_is_true(show_compoundword)){
		$this.attr('title', co_title);
		$this.attr('title2', wo_title);
	} else {
		$this.attr('title', wo_title);
		$this.attr('title2', co_title);
	}
}

/* called by update_status (for Cliked tooltip)
 change the number of word 'TO DO' at the top of text_read.html*/
function update_workcount(){
	// Counting the words without duplicate???
	// get all the wordtext element with status 0
	var DOCUMENT = window.DOCUMENT;
	var status0_words = DOCUMENT.find('span[woid][iscompoundword="False"][wostatus=0]');
	var wordtext_list = [];
	status0_words.each(function(idx, val){
		wordtext_list.push($(val).attr('wowordtext').toLowerCase());
	});
	// count how many occurences for each word
	var counts = {}; //it will be : {1, 1, 1, 1, 2, 1, 1, etc...}
	for (var i = 0; i < wordtext_list.length; i++) {
		counts[wordtext_list[i]] = 1 + (counts[wordtext_list[i]] || 0);
	} 
	// sum up all these different occurences
	var todo_wordcount = Object.keys(counts).length;

	// and in percent:
	var texttotalword = $('#todo_wordcount_pc').data('texttotalword');
	if (texttotalword != 0){ 
		var todo_wordcount_pc = Math.round( todo_wordcount*100/texttotalword );
	} else {
		var todo_wordcount_pc = 0; // case of opening a webpage for the first time
	}

	// displaying it
	$('#todo_wordcount').html('&nbsp;'+todo_wordcount.toString()+'&nbsp;');
	$('#todo_wordcount_pc').html(todo_wordcount_pc.toString());
	// and change the color if necessary:
	if (todo_wordcount == 0){
		$('#todo_wordcount_AND_pc').attr('wostatus','1'); 
		// and disable the 'i know all' button
		$('button#iknowall').attr('disabled','');
	} else {
		$('#todo_wordcount_AND_pc').attr('wostatus','0'); }
}