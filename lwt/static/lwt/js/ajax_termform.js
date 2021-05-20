/* Submitting a form for the termform func in termform.py 
   @op	: can be ´edit´, ´new´, and ´similar´ (to copy a similar word)
   @wo_id : id of the word selected
   @simwo_id : optional. id of the chosen similar word

   called by:  - clicking on submit button in form of the top right (or using shortcut keyboard)
							called by newwordform_new_or_edit: op == 'new' or 'edit'
			   - clicking on the ´plus´ to signify it´s a similar word in the top right panel
									(or using keyboard shortcut) op == 'similar'
*/ 
function ajax_submit_word(event, op, wo_id, language_id, simwo_id=null){
	// The Submit button could be intented from the termform searchbox though : if the User
	// presses Enter but meants to launch the searchbox, not submit the word...
	// Detect if the User has put focus on the search box: It's more an error from the User
	// than a bug of the program but we are tolerant for this...
	
	// if op==similar, it means the keyboard shortcut (or click on the link)has been pressed. 
	//it's evidently not a request for the searchbox then...
	if (op != 'similar' && $("#topright #termformSearchbox").is(":focus")){
		submit_termformSearchbox(wo_id, language_id);	
	} else {
		var token =  $("#newwordform").find('input[name=csrfmiddlewaretoken]').val(); // Indispensable. Get the csrf already defined in the form
		var data_to_go = {}; // get the individual data of the form, then we'll JSON.stringify them.
		data_to_go['translation'] = $("textarea[name=translation]").val();
		data_to_go['sentence'] = $("textarea[name=customentence]").val();
		data_to_go['status'] = $("input[name=status]:checked").val();
		data_to_go['romanization'] = $("input[name=romanization]").val();
		data_to_go['wordtags'] = $("input[name=wordtags]").val();
		//NOTE: compoundword_id_list cariable is directly embedded in 'termform_new_or_edit.html'
		// extra_field:
		var extra_field = '[';
		$("#div_id_extra_field input").each(function(idx, el){
			if (idx != 0){
				extra_field += ',';
			}
			var k = $(this).attr('name');
			var v = $(this).val();
			extra_field += '{"' + k + '":"'+ v +'"}'; 
		});
		extra_field += ']';
		//console.log(extra_field);
		data_to_go['extra_field'] = extra_field;
		
		var redefine_only_this_word = $("input[name=redefine_only_this_word]:checked").val();
		$.ajax({url: '/termform/', 
				type: 'POST',
				dataType: 'json',
				data: 
					{ 
						'newwordform': JSON.stringify(data_to_go),
						'csrfmiddlewaretoken': token,
						'op': op,
						'wo_id': wo_id,
						'simwo_id': simwo_id,
						'redefine_only_this_word': redefine_only_this_word,
						'compoundword_id_list': JSON.stringify(compoundword_id_list),
					},
				success: function(data){ 
					$('#newwordform').replaceWith(data['html']);
					update_data_of_wo_cowo_and_sims(data, op);
					$('#bottomleft').focus(); //and set the focus to the text again (useful for keyboard shortcuts)
					//update the tooltip for the word also
					var sel_word = $('.clicked');
					click_ctrlclick_toggle(sel_word, event, 'update_tooltip');
					},
				error : function(data , status , xhr){ console.log('ERROR'); console.log(data); console.log(status); console.log(xhr); }
		});
	}
}

/* not used in fact. It was used to AJAX search similar word */
function toggle_show_similarword() {
	/* checkbox 'show also words defined elsewhere */
	if ($('#show_knownword_checkbox').is(':checked')){ 
		$('.possible_similarword[wostatus!=0]').parent().removeClass('hidden');} 
	 else { 
		$('.possible_similarword[wostatus!=0]').parent().addClass('hidden');}  // we select the <li> whose child is <a> with wostatus="0"
}

/* called by inline call onclick in ajax_text_read.js */
/* @e	: the element given by '$.each(possiblesimilarword, function(key, val){'
/* @simvo_id	: the id of the similar word found
/* @wo_id		: the id of the current word */
function toggle_makeit_similarword(e, simwo_id, wo_id){
	if ($(e).hasClass('chosen_similarword')) { 
		$(e).removeClass('chosen_similarword'); // put a css to make it clear that it has been chosen
		$('select[name="chosen_similarword"] option[value="'+simwo_id+'"]').remove();
	} else {
		$(e).addClass('chosen_similarword');
		$('select[name="chosen_similarword"]').append($('<option>', {value : simwo_id, selected: true})); // put it inside the selectmultiple checkbox
		}
}


/* helper func for ajax_clicked_word and ajax_ctrlclicked_compoundword 
    Display the list of possible similar words:    */
function _display_possiblesimilarword(data, wo_id){
	var possiblesimilarword = data['possiblesimilarword'];

	// display the possible similar words
	r = '<p>'+ gettext('Possible similar words ?')+'<br>';
	if ($.isEmptyObject(possiblesimilarword)){
		r += gettext('No similar words found.');
	} else {
		r += '<ul class="fa-ul">';
		$.each(possiblesimilarword, function(key, val){
			r += '<li ';
			r += '> <span simwo_id="'+val.id+'" href="#" data=toggle="tooltip" class="possible_similarword" ';
			r += ' wostatus='+ val.status +
				' onClick="ajax_submit_word(event, \'similar\','+val.id+', null, '+wo_id+');return false;"'+
				' title="'+gettext('Click if you want to consider this as the same word in fact (i.e = &#39similar&#39 word)')+'">'+
				'<i class="fa fa-plus-circle" aria-hidden="true"></i> '+
				val.wordtext +'</span>';
			if (val.translation){ r += ' (= '+val.translation+')'; }
			r += ' ['+gettext('in : ')+'"'+val.customsentence+'"]'+
				' <span class="text-muted kb_short_'+(key+1)+'" data-simwo_id="'+val.id+'" title="'+gettext('Number keyboard shortcut')+'">['+(key+1)+']</span></li>';
		});
		r += '</ul>';
	}
	r += '</p>';
	return r;
}

/* clicking on 'go' in the termform searchbox (to search other word) */
function submit_termformSearchbox(wo_id, language_id){
	var searched_word = $('#termformSearchbox').val();	
	if (dictwebpage_searched_word != ''){
		// search in the dictionary with the text given
		_clicked_weblink_radiobutton(searched_word);
		// search similar word with the text given 
		// it can be a compound word: the user has written firstword secondword ...
		searched_word_list = searched_word.split(' ');
		if (searched_word_list.length == 1){
			$.ajax({url: '/search_possiblesimilarword/', type: 'GET',
			data: {
					'searchboxtext' : searched_word, 
					'language_id': language_id
					},
			success: function(data){
				var data = JSON.parse(data);
				var r = _display_possiblesimilarword(data, wo_id);
				$('#result_possiblesimilarword').html(r);
			},
			 error : function(data , status , xhr){ console.log(data); console.log(status); console.log(xhr);}
			});
		} else { //it's a compound word
			$.ajax({url: '/search_possiblesimilarCompoundword/', type: 'GET',
			data: {
					'firstsearch_el' : firstsearch_el, 
					'secondsearch_el' : secondsearch_el, 
					'language_id': language_id
					},
			success: function(data){
				var data = JSON.parse(data);
				var r = _display_possiblesimilarword(data, wo_id);
				$('#result_possiblesimilarword').html(r);
			},
			 error : function(data , status , xhr){ console.log(data); console.log(status); console.log(xhr);}
			});
		}
	}
}


/* NOT USED finally */
/* make a word similar to another one or undo this action (it deletes the word in fact) */
/*
function ajax_create_or_del_similarword(simwo_id, op, wo_id) {
	$.ajax({url: '/create_or_del_similarword/', 
			type: 'GET',
			dataType: 'json',
			data: 
				{ 
					'wo_id':wo_id, 'op': op, 'simwo_id': simwo_id,
				},
			success: function(data){ 
				if (op == 'create'){ // creating the similar word
				// updating the hovering tooltip:
				update_status(simwo_id, 'edit', data['simwostatus']);
				update_romanization(simwo_id, 'edit', data['simworomanization']);
				update_translation(simwo_id, 'edit', data['simwotranslation']);
				// make a green color to show that it was updated:
				$('a[simwo_id='+simwo_id+']').attr("class","similarword"); 
				$('a[simwo_id='+simwo_id+']').attr('onClick','ajax_create_or_del_similarword('+simwo_id+',\'del\',\''+
						wo_id+'\');return false;'); 
				$('a[simwo_id='+simwo_id+']').attr('title',gettext('Click to make it not a similar word (i.e Deleting word)')); 

				} else if (op == 'del'){ // deleting the similar word
				// updating the hovering tooltip:
				update_status(simwo_id, 'edit', '0');
				update_romanization(simwo_id, 'edit', '');
				update_translation(simwo_id, 'edit', '');
				// remove the green color:
				$('a[simwo_id='+simwo_id+']').attr("class","notsimilarword"); 
				$('a[simwo_id='+simwo_id+']').attr('onClick','ajax_create_or_del_similarword('+simwo_id+',\'create\',\''+
						wo_id+'\');return false;'); 
				$('a[simwo_id='+simwo_id+']').attr('title',gettext('Click if you want to consider this as the same word in fact (i.e = &#39similar&#39 word)')); 
				}
			},
			error : function(data , status , xhr){ console.log('ERROR'); console.log(data); console.log(status); console.log(xhr); }
	});
}
*/

/* Not used in fact. AJAX is not the way I think */
/*
function ajax_search_possiblesimilarword(wo_id, searchboxtext){
	// called by newwordform_new_or_edit:
	 //show a list of words, which could be similar to the given word 
	$.ajax({
		url: '/search_possiblesimilarword',
		type: 'GET',
		data: {'wo_id': wo_id, 'searchboxtext': searchboxtext},
		success: function(data){
			var data_json = JSON.parse(data); 
			var possiblesimilarword = data_json['possible_similarword'];
			var alreadyaddedsimilarword = data_json['alreadyadded_similarword'];
			
			// display the possible similar words
			r = '<p>'+ gettext('Possible similar words: ')+'<br>';
			if ($.isEmptyObject(possiblesimilarword)){
				r += gettext('Nothing here.');
			} else {
				r += '<input type="checkbox" id="show_knownword_checkbox" onChange="toggle_show_similarword()" ';
				r += '>show also words defined elsewhere</input> ';
				var initialval = ''; // used to check distinct val
				r += '<ul class="fa-ul">';
				$.each(possiblesimilarword, function(key, val){
					if (val.wordtext != initialval){ // remove duplicate
					r += '<li ';
					if (val.status != 0){ r += 'class="hidden" ';}
					r += '><i class="fa fa-plus-circle" aria-hidden="true" data-container="body" data-toggle="tooltip" '+
						' title="'+gettext('Click if you want to consider this as the same word in fact (i.e = &#39similar&#39 word)')+'"'+
						'></i> <span simwo_id="'+val.id+'" href="#" data=toggle="tooltip" class="possible_similarword" ';
					r += ' wostatus='+ val.status +
						' onClick="toggle_makeit_similarword(this,'+val.id+','+wo_id+');return false;"'+
//						' onClick="ajax_create_or_del_similarword('+val.id+',\'create\',\''+wo_id+'\');return false;"'+
						' title="'+gettext('Click if you want to consider this as the same word in fact (i.e = &#39similar&#39 word)')+'">'+
						val.wordtext +'(= '+val.translation+') ('+gettext('in text') + ': "' + val.text__title + '")</span></li>';
					initialval = val.wordtext;}
					else {initialval = val.wordtext;}// remove duplicate
				});
				r += '</ul>';
			}
			r += '</p>';
			$('#result_possiblesimilarword').html(r);

			// display the already added similar words
			var r = '<p>' +gettext('Already added similar words:') +'<br>';
			if ($.isEmptyObject(alreadyaddedsimilarword)){
				r += gettext('Nothing here.');}
			else {
				r += '<ul>';
				$.each(alreadyaddedsimilarword, function(key, val){
					if (val.wordtext != initialval){ // remove duplicate
					r += '<li><a simwo_id="'+val.id+'" href="#" data=toggle="tooltip" '+
						'onClick="ajax_create_or_del_similarword('+val.id+',\'del\',\''+wo_id+'\');return false;"'
					// make it visually a similar word:
					r += ' class="similarword" title="Click to make it not a similar word (i.e Deleting word)"'+ 
						'>'+ val.wordtext + ' ('+gettext('in text') + ': "' + val.text__title + '")</a></li>';

					initialval = val.wordtext;}
					else {initialval = val.wordtext;}// remove duplicate
				});
				r += '</ul>';
				}
				r += '</p>';
				$('#result_alreadyaddedsimilarword').html(r);

		}
	});
}
*/



/* NOT USED finally */
/* called by newwordform_new_or_edit:
 show a list of sentences where the textitem appears at the end of the form */
/*
function ajax_showsentence(wo_ids, tick_button_url){
	$.ajax({
		url: '/show_sentence/',
		type: 'GET',
		data: { 'wo_ids': JSON.stringify(wo_ids) },
		success: function(data) {
			var r = '';
			r += gettext('(Click on ')+'<img src="'+tick_button_url+'" title="{% trans "Choose" %}" alt="Choose" /> '+gettext('to copy sentence into above term')+'</p>';
			var sentences = JSON.parse(data);
			r += '<p>';
			$.each(sentences, function(key, val) {
				r += '<span onclick="$(\'#id_sentence\').val($(\'#id_sentence\').val()+\'\\n\'+\''+val[1]+'\')"><img src="'+
				tick_button_url+'" title="'+gettext('Choose')+'" alt="Choose" /></span>&nbsp;';
				r += '<span title="Click to open the text: \''+val[0][1]+'\'"';
				r += 'onclick="document.location=\'/text_read/'+val[0][0]+'\';">'+val[1]+'</span><br />';
				});
			r += '</p>';
			$('#result_sentence').html(r);
		},
		error : function(data , status , xhr){ console.log('ERROR'); console.log(data); console.log(status); console.log(xhr); }
	});
}
*/