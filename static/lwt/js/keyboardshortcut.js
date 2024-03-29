
/* helper functions for the arrow key navigating */
function _is_word(input){
	var woid_attr = input.attr('woid');
	// For some browsers, `attr` is undefined; for others,
	// `attr` is false.  Check for both.
	if (typeof woid_attr !== 'undefined' && woid_attr !== false) {
		return true;
	} else {
		return false;
	}
}
function _is_in_text(input){
	if (input.is('span')) {
		return true;
	} else {
		return false;
	}
}

function initialize_to_selectedword(sel_word, e){
	if (sel_word.length != 0){
		var prev_unknown_word = _prev(sel_word);
		while(_is_in_text(prev_unknown_word) ){
			if (_is_word(prev_unknown_word)){
				sel_word = prev_unknown_word;
				break;
			} else {
				var possible_prev_unknown_word = _prev(prev_unknown_word);
				if (prev_unknown_word == possible_prev_unknown_word){
					break;
				}
				prev_unknown_word = possible_prev_unknown_word;
			}
		}
		// auto scroll to this word:
		$('#bottomleft').animate({
			scrollTop: (sel_word.offset().top - $( window ).height()*1/3)
		}, 800);
		
		
		// set the focus when clicking back into the text zone
		/* NOT USED finally
		$( "#bottomleft" ).bind( "click", function(e) {
			  $( this ).focus();
			e.preventDefault();
		}); */
		
		//case where we open a brand new text. The word selected will be a unknown word
		// therefore, make it like I click on it.
		if (sel_word.attr('wostatus') == 0){
			click_ctrlclick_toggle(sel_word, e); // creating: clicktooltip and the right panel (bottom & top)
			sel_word.addClass('clicked'); 
		} else {
			sel_word.addClass('clicked'); 
			//sel_word.addClass('firstword');  Useful???
		}
		// give the focus to the text since it allows to use the keyboard shorcuts
		$("#bottomleft").focus();
	}
}

// auto scroll when moving with the keyboard arrow ->, after "I know all" :
function _autoscroll_to_sel_word(sel_word){
	var scrollY = sel_word.offset().top - $( window ).height()*1/3;
	if (sel_word.offset().top > $( window ).height()*2/3){
		$('#bottomleft').animate({
			scrollTop:  '+='+scrollY.toString()+'px'
		}, 800);
	}
}

/* it's a custom Obj.next() which is able to jump to a next webpage section  */
function _next(word){
	var DOCUMENT = window.DOCUMENT;
	if (TEXTTYPE == 'text'){
		return word.next();
	} else if (TEXTTYPE == 'html' || TEXTTYPE == 'doc'){
		if (word.is(':last-child')){
			var curr_wps_nb = word.parent().data('webpagesection');
			var all_webpagesection = DOCUMENT.find('.webpage_done');
			var found_curr_wps = false;
			var next_webpagesection = null;
			for (let wps of all_webpagesection){
				if (found_curr_wps){
					var next_webpagesection = $(wps);					
					break
				}
				if ($(wps).data('webpagesection') == curr_wps_nb){
					found_curr_wps = true; // at the next iteration, it will be the wps we want
				}
			}
			// check whether the current wps wasn't the last wps of the webpage in fact
			if (next_webpagesection != null){
				var next_word = next_webpagesection.find(":first-child");
				return next_word;
			} else {
				return word;
			}
		} else {
			return word.next();
		}	
	}
}

/* it's a custom Obj.prev() which is able to jump to a previous webpage section  */
function _prev(word){
	var DOCUMENT = window.DOCUMENT;
	if (TEXTTYPE == 'text'){
		return word.prev();
	} else if (TEXTTYPE == 'html' || TEXTTYPE == 'doc'){
		/*
		return word.prev();
		*/
		if (word.is(':first-child')){
			var curr_wps = $(word.parent());
			var curr_wps_nb = word.parent().data('webpagesection');
			var all_webpagesection = DOCUMENT.find('.webpage_done');
			var prev_webpagesection = curr_wps;
			for (let wps of all_webpagesection){
				if ($(wps).data('webpagesection') == curr_wps_nb){
					break;
				}
				prev_webpagesection = $(wps);					
			}
			// check whether the current wps wasn't the last wps of the webpage in fact
			if (prev_webpagesection != curr_wps){
				var prev_word = prev_webpagesection.find(":last-child");
				return prev_word;
			} else {
				return word;
			}
		} else {
			return word.prev();
		}	
	}
}

/* helper function to navigate (it's also used in ajax_termform after a word has been submitted) */
function _move_next_word(sel_word, e){
	sel_word.removeClass('clicked'); //unselect the current word
	//sel_word.removeClass('firstword'); //unselect the current word Useful???
	var next_word = _next(sel_word);
	while(_is_in_text(next_word)){
		if (_is_word(next_word) && next_word.attr('wostatus')==0){
			sel_word = next_word;
			break;
		} else {
			next_word = _next(next_word);
		}
	}

	_autoscroll_to_sel_word(sel_word);

	sel_word.addClass('clicked'); //select the next word
	//click_ctrlclick_toggle(sel_word, e); // creating: clicktooltip and the right panel (bottom & top)
	if (sel_word.attr('wostatus') == "0"){
		var op = 'new';
	} else {
		var op = 'edit';
	}
	// we interrupt the previous request if it exists
	if(typeof $ajaxClickedWord !== 'undefined'){
		$ajaxClickedWord.abort();
	}
	$ajaxClickedWord = ajax_clicked_word(sel_word.attr('woid'), sel_word.attr('show_compoundword'), op, null);
}

/* helper function to detect the keypress outof the focus of the termform */
function _toprightInputBoxes_have_focus(){
	has_focus = false;	
	if ($("#topright #id_translation").is(":focus") ||
		$("#topright #id_wordtags_tags_input_tag").is(":focus") ||
		$("#topright #id_sentence").is(":focus") ||
		$("#topright #termformSearchbox").is(":focus")){
		has_focus = true;		
	}
	return has_focus;
}

function key_binding(DOCUMENT, e){
	// case for MacOS because keybinding is different for AltGr:
	var is_Mac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;

	/*********************************************************/
	/*          MOVING                                       */
	/*********************************************************/
	var DOCUMENT = window.DOCUMENT;
	DOCUMENT.keydown(function(e) { // only keydown is able to get the arrow keys... (strange)
		//the current selected word:
		var sel_word = DOCUMENT.find('.clicked');

		var ev = e || window.event;
		var keydown = ev.keyCode || ev.which;

		// → arrow right
		if (keydown == '39' && !_toprightInputBoxes_have_focus()){ 
			_move_next_word(sel_word, e);
			ev.preventDefault();
		}

		// ← arrow left
		if (keydown == '37' && !_toprightInputBoxes_have_focus()){ 
			sel_word.removeClass('clicked'); //unselect the current word
			//sel_word.removeClass('firstword'); //unselect the current word USEFUL???
			var prev_word = _prev(sel_word);
			while(_is_in_text(prev_word)){
				if (_is_word(prev_word)){
					sel_word = prev_word;
					break;
				} else {
					prev_word = _prev(prev_word);
				}
			}
			sel_word.addClass('clicked'); //select the previous word
			//click_ctrlclick_toggle(sel_word, e); // creating: clicktooltip and the right panel (bottom & top)
			if (sel_word.attr('wostatus') == "0"){
				var op = 'new';
			} else {
				var op = 'edit';
			}
			ajax_clicked_word(sel_word.attr('woid'), sel_word.attr('show_compoundword'), op, null);

			ev.preventDefault();
		}
	});
		
	DOCUMENT.keypress(function(e) { //only keypress can get combination like Shift+letter
		//the current selected word:
		var sel_word = DOCUMENT.find('.clicked');
		var ev = e || window.event;
		var keypress = ev.keyCode || ev.which;
		//console.log(keypress);
		//do stuff with "key" here...
				
	/*********************************************************/
	/*          BOTTOM LEFT PANEL                            */
	/*********************************************************/
		// 'a': I know this term well
		if (keypress == '97' && !_toprightInputBoxes_have_focus()){ 
			 //console.log('A is pressed');
			ajax_update_status(e, sel_word.attr('woid'), 'wellkwn');
			_move_next_word(sel_word, e);
		}
		
		// 's': Ignore this term
		if (keypress == '115' && !_toprightInputBoxes_have_focus()){ 
			ajax_update_status(e, sel_word.attr('woid'), 'ignored');
			_move_next_word(sel_word, e);
		}
		
		// 'd': link dict1
		if (keypress == '100' && !_toprightInputBoxes_have_focus()){ 
			ajax_dictwebpage(WBLINK1, sel_word.attr('wowordtext'),'');
			$('input#dict1uri[type="radio"]').prop('checked', true);
		}
		
		// 'D': link dict2
		if (keypress == '68' && !_toprightInputBoxes_have_focus()){ 
			ajax_dictwebpage(WBLINK2, sel_word.attr('wowordtext'),'');
			$('input#dict2uri[type="radio"]').prop('checked', true);
		}
		
		// 'g': link gogle word
		if (keypress == '103' && !_toprightInputBoxes_have_focus()){ 
			ajax_dictwebpage(WBLINK3, sel_word.attr('wowordtext'),'');
			$('input#wo_gtr[type="radio"]').prop('checked', true);
		}
		
		// 'G': link google sentence
		if (keypress == '71' && !_toprightInputBoxes_have_focus()){ 
			ajax_dictwebpage(WBLINK3, sel_word.attr('wowordtext'), sel_word.attr('woid'));
			$('input#sent_gtr[type="radio"]').prop('checked', true);
		}

		// 'AltGr+k': mark all the words in the current sentence as known
		if (
			((!is_Mac && keypress == '339') || (is_Mac && keypress == '730'))
					&& !_toprightInputBoxes_have_focus()){ 
			iknowall(sel_word.attr('woid'));
			e.preventDefault();
		}
		
	/*********************************************************/
	/*          TOOLTIP                                      */
	/*********************************************************/
		// 'e': edit this word
		if (keypress == '101' && !_toprightInputBoxes_have_focus()){ 
			tooltip_ajax_termform(sel_word.attr('woid'),'edit','');
			ajax_dictwebpage(WBLINK1, sel_word.attr('wowordtext'),'');
		}
		
	/*********************************************************/
	/*          TOPRIGHT PANEL                               */
	/*********************************************************/
		// 'altGr+t': focus on translate input box
		if ((!is_Mac && keypress == '254') || (is_Mac && keypress == '8224')){ 
			$('#id_translation').focus();
			event.preventDefault();
		}

		// 'altGr+w': focus on search other spelling input box
		if ((!is_Mac && keypress == '229') || (is_Mac && keypress == '8721')){ 
			$('#termformSearchbox').focus();
			event.preventDefault();
		}

		// 'altGr+d': toggle focus on the bottom right dictionary. Again pressed, toggle to similar words result
		if ((!is_Mac && keypress == '273') || (is_Mac && keypress == '8706')){ 
			var current_sim_OR_dict_highlight = $('.sim_OR_dict_highlight');
			if (current_sim_OR_dict_highlight.attr('id') == 'possible_similarword_result'){
				$('#bottomright').addClass('sim_OR_dict_highlight');
				$('#possible_similarword_result').removeClass('sim_OR_dict_highlight');
			} else {
				$('#possible_similarword_result').addClass('sim_OR_dict_highlight');
				$('#bottomright').removeClass('sim_OR_dict_highlight');
			}
			event.preventDefault();
		}

		// '1': choose the first similar word
		if (keypress == '49' && !_toprightInputBoxes_have_focus() && 
							$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var wo_id = $('.kb_short_'+'1').data('simwo_id');
			ajax_submit_word(event, 'similar', wo_id, null, sel_word.attr('woid'));
		}

		// '2': choose the second similar word
		if (keypress == '50' && !_toprightInputBoxes_have_focus() && 
						$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var wo_id = $('.kb_short_'+'2').data('simwo_id');
			ajax_submit_word(event, 'similar', wo_id, null, sel_word.attr('woid'));
		}

		// '3': choose the third similar word
		if (keypress == '51' && !_toprightInputBoxes_have_focus() &&
						$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var wo_id = $('.kb_short_'+'3').data('simwo_id');
			ajax_submit_word(event, 'similar', wo_id, null, sel_word.attr('woid'));
		}

		// '4': choose the fourth similar word
		if (keypress == '52' && !_toprightInputBoxes_have_focus() &&
								$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var wo_id = $('.kb_short_'+'4').data('simwo_id');
			ajax_submit_word(event, 'similar', wo_id, null, sel_word.attr('woid'));
		}

		// '5': choose the fifth similar word
		if (keypress == '53' && !_toprightInputBoxes_have_focus() &&
								$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var wo_id = $('.kb_short_'+'5').data('simwo_id');
			ajax_submit_word(event, 'similar', wo_id, null, sel_word.attr('woid'));
		}
		// '6': choose the sixth similar word
		if (keypress == '54' && !_toprightInputBoxes_have_focus() &&
								$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var wo_id = $('.kb_short_'+'6').data('simwo_id');
			ajax_submit_word(event, 'similar', wo_id, null, sel_word.attr('woid'));
		}
		// '7': choose the seventh similar word
		if (keypress == '55' && !_toprightInputBoxes_have_focus() &&
								$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var wo_id = $('.kb_short_'+'7').data('simwo_id');
			ajax_submit_word(event, 'similar', wo_id, null, sel_word.attr('woid'));
		}
		// '8': choose the eighth similar word
		if (keypress == '56' && !_toprightInputBoxes_have_focus() &&
								$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var wo_id = $('.kb_short_'+'8').data('simwo_id');
			ajax_submit_word(event, 'similar', wo_id, null, sel_word.attr('woid'));
		}
		// '9': choose the ninth similar word
		if (keypress == '57' && !_toprightInputBoxes_have_focus() &&
								$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var wo_id = $('.kb_short_'+'9').data('simwo_id');
			ajax_submit_word(event, 'similar', wo_id, null, sel_word.attr('woid'));
		}

		// 'altGr+a': submit the form to save the word´s definition
		if ((!is_Mac && keypress == '225') || (is_Mac && keypress == '229')){ 
			$('#submit_word').trigger('click');
			event.preventDefault();
		}
	/*********************************************************/
	/*          BOTTOMRIGHT PANEL                               */
	/*********************************************************/
		// '1': choose the first translation
		if (keypress == '49' && !$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var trans_item_1 = $('#trans_item_1').text();
			addTranslation(trans_item_1);
			event.preventDefault(); // else it's writing the number inside the translation area
			$('#id_translation').focus();
		}

		// '2': choose the 2nd translation
		if (keypress == '50' && !$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var trans_item_2 = $('#trans_item_2').text();
			addTranslation(trans_item_2);
			event.preventDefault(); // else it's writing the number inside the translation area
			$('#id_translation').focus();
		}
		// '3': choose the 3rd translation
		if (keypress == '51' && !$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var trans_item_3 = $('#trans_item_3').text();
			addTranslation(trans_item_3);
			event.preventDefault(); // else it's writing the number inside the translation area
			$('#id_translation').focus();
		}
		// '4': choose the 4th translation
		if (keypress == '52' && !$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var trans_item_4 = $('#trans_item_4').text();
			addTranslation(trans_item_4);
			event.preventDefault(); // else it's writing the number inside the translation area
			$('#id_translation').focus();
		}
		// '5': choose the 5th translation
		if (keypress == '53' && !$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var trans_item_5 = $('#trans_item_5').text();
			addTranslation(trans_item_5);
			event.preventDefault(); // else it's writing the number inside the translation area
			$('#id_translation').focus();
		}
		// '6': choose the 6th translation
		if (keypress == '54' && !$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var trans_item_6 = $('#trans_item_6').text();
			addTranslation(trans_item_6);
			event.preventDefault(); // else it's writing the number inside the translation area
			$('#id_translation').focus();
		}
		// '7': choose the 7th translation
		if (keypress == '55' && !$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var trans_item_7 = $('#trans_item_7').text();
			addTranslation(trans_item_7);
			event.preventDefault(); // else it's writing the number inside the translation area
			$('#id_translation').focus();
		}
		// '8': choose the 8th translation
		if (keypress == '56' && !$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var trans_item_8 = $('#trans_item_8').text();
			addTranslation(trans_item_8);
			event.preventDefault(); // else it's writing the number inside the translation area
			$('#id_translation').focus();
		}
		// '9': choose the 9th translation
		if (keypress == '57' && !$('#possible_similarword_result').hasClass('sim_OR_dict_highlight')){ 
			var trans_item_9 = $('#trans_item_9').text();
			addTranslation(trans_item_9);
			event.preventDefault(); // else it's writing the number inside the translation area
			$('#id_translation').focus();
		}
	});
}

