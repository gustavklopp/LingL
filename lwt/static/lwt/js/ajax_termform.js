/* ALL FUNCTIONS called by interacting with the termform :
        the top-right section in text_read.html */

function ajax_submit_word(op, wo_id){
	/* called by newwordform_new_or_edit:
	 submit the form to create or edit a word */
	var token =  $("#newwordform").find('input[name=csrfmiddlewaretoken]').val(); // Indispensable. Get the csrf already defined in the form
	var data_to_go = {}; // get the individual data of the form, then we'll JSON.stringify them.
	data_to_go['translation'] = $("textarea[name=translation]").val();
	data_to_go['sentence'] = $("textarea[name=customentence]").val();
	data_to_go['status'] = $("input[name=status]:checked").val();
	data_to_go['romanization'] = $("input[name=romanization]").val();
	data_to_go['wordtags'] = $("input[name=wordtags]").val();
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
	
	var chosen_similarword = [];
	$.each($("select[name=chosen_similarword] option:selected"), function(){
		chosen_similarword.push($(this).val());
	});
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
					'chosen_similarword': JSON.stringify(chosen_similarword),
					'redefine_only_this_word': redefine_only_this_word,
					'compoundword_id_list': JSON.stringify(compoundword_id_list),
				},
			success: function(data){ 
				$('#newwordform').replaceWith(data['html']);
				ajax_update_word_simword_compoundword(data, op);
				},
			error : function(data , status , xhr){ console.log('ERROR'); console.log(data); console.log(status); console.log(xhr); }
	});
}

function toggle_show_similarword() {
	/* checkbox 'show also words defined elsewhere */
	if ($('#show_knownword_checkbox').is(':checked')){ 
		$('.possible_similarword[wostatus!=0]').parent().removeClass('hidden');} 
	 else { 
		$('.possible_similarword[wostatus!=0]').parent().addClass('hidden');}  // we select the <li> whose child is <a> with wostatus="0"
}

function toggle_makeit_similarword(e,simwo_id,wo_id){
	if ($(e).hasClass('chosen_similarword')) { 
		$(e).removeClass('chosen_similarword'); // put a css to make it clear that it has been chosen
		$('select[name="chosen_similarword"] option[value="'+simwo_id+'"]').remove();
	} else {
		$(e).addClass('chosen_similarword');
		$('select[name="chosen_similarword"]').append($('<option>', {value : simwo_id, selected: true})); // put it inside the selectmultiple checkbox
		}
}

function ajax_search_possiblesimilarword(wo_id, searchboxtext){
	/* called by newwordform_new_or_edit:
	 show a list of words, which could be similar to the given word */
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
						val.wordtext + ' ('+gettext('in text') + ': "' + val.text__title + '")</span></li>';
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

function ajax_create_or_del_similarword(simwo_id, op, wo_id) {
	/* make a word similar to another one or undo this action (it deletes the word in fact) */
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

function ajax_showsentence(wo_ids, tick_button_url){
	/* called by newwordform_new_or_edit:
	 show a list of sentences where the textitem appears at the end of the form */
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