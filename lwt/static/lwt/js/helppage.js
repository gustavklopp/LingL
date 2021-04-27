/* helper func for the arrow key navigating */
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

/* make sure that a word is selected at the start (else the shortcuts can't work) */
/* (just before the first unknown word, except if it´s the first of the text) */
$(document).ready(function(e) {
	//select the word before the first unknown word as the start
	var sel_word = $('#thetext span[wostatus="0"]').first(); //it´s an unknown word
	var prev_unknown_word = sel_word.prev();
	while(_is_in_text(prev_unknown_word)){
		if (_is_word(prev_unknown_word)){
			sel_word = prev_unknown_word;
			break;
		} else {
			prev_unknown_word = prev_unknown_word.prev()
		}
	}
	sel_word.addClass('clicked'); 
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
	}
	// give the focus to the text since it allows to use the keyboard shorcuts
	$("#bottomleft").focus();
});

/* helper function to navigate (it's also used in ajax_termform after a word has been submitted) */
function _move_next_word(sel_word, e){
	sel_word.removeClass('clicked'); //unselect the current word
	var next_word = sel_word.next();
	while(_is_in_text(next_word)){
		if (_is_word(next_word) && next_word.attr('wostatus')==0){
			sel_word = next_word;
			break;
		} else {
			next_word = next_word.next()
		}
	}
	sel_word.addClass('clicked'); //select the next word
	click_ctrlclick_toggle(sel_word, e); // creating: clicktooltip and the right panel (bottom & top)
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

$(function() {

	/*********************************************************/
	/*          MOVING                                       */
	/*********************************************************/
	$(window).keydown(function(e) { // only keydown is able to get the arrow keys... (strange)
		//the current selected word:
		var sel_word = $('.clicked');

		var ev = e || window.event;
		var keydown = ev.keyCode || ev.which;

		// arrow right
		if (keydown == '39' && !_toprightInputBoxes_have_focus()){ 
			_move_next_word(sel_word, e);
		}

		// arrow left
		if (keydown == '37' && !_toprightInputBoxes_have_focus()){ 
			sel_word.removeClass('clicked'); //unselect the current word
			var prev_word = sel_word.prev();
			while(_is_in_text(prev_word)){
				if (_is_word(prev_word)){
					sel_word = prev_word;
					break;
				} else {
					prev_word = prev_word.prev()
				}
			}
			sel_word.addClass('clicked'); //select the previous word
			click_ctrlclick_toggle(sel_word, e); // creating: clicktooltip and the right panel (bottom & top)
		}
	});
		
	$(window).keypress(function(e) { //only keypress can get combination like Shift+letter
		//the current selected word:
		var sel_word = $('.clicked');
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
		}
		
		// 'D': link dict2
		if (keypress == '68' && !_toprightInputBoxes_have_focus()){ 
			ajax_dictwebpage(WBLINK2, sel_word.attr('wowordtext'),'');
		}
		
		// 'g': link gogle word
		if (keypress == '103' && !_toprightInputBoxes_have_focus()){ 
			ajax_dictwebpage(WBLINK3, sel_word.attr('wowordtext'),'');
		}
		
		// 'G': link google sentence
		if (keypress == '71' && !_toprightInputBoxes_have_focus()){ 
			ajax_dictwebpage(WBLINK3, sel_word.attr('wowordtext'), sel_word.attr('woid'));
		}

		// 'AltGr+k': mark all the words in the current sentence as known
		if (keypress == '339' && !_toprightInputBoxes_have_focus()){ 
			iknowall(sel_word.attr('woid'));
			event.preventDefault();
		}
		
	/*********************************************************/
	/*          TOOLTIP                                      */
	/*********************************************************/
		// 'e': edit this word
		if (keypress == '101' && !_toprightInputBoxes_have_focus()){ 
			ajax_termform(sel_word.attr('woid'),'edit','');
			ajax_dictwebpage(WBLINK1, sel_word.attr('wowordtext'),'');
		}
		
	/*********************************************************/
	/*          TOPRIGHT PANEL                               */
	/*********************************************************/
		// 'altGr+t': focus on translate input box
		if (keypress == '254'){ 
			$('#id_translation').focus();
			event.preventDefault();
		}

		// 'altGr+s': focus on search other spelling input box
		if (keypress == '353'){ 
			$('#termformSearchbox').focus();
			event.preventDefault();
		}

		// '1': choose the first similar word
		if (keypress == '49' && !_toprightInputBoxes_have_focus()){ 
			var wo_id = $('.kb_short_'+'1').data('simwo_id');
			ajax_submit_word(event, 'similar', wo_id, null, sel_word.attr('woid'));
			_move_next_word(sel_word, e);
		}

		// '2': choose the second similar word
		if (keypress == '50' && !_toprightInputBoxes_have_focus()){ 
			var wo_id = $('.kb_short_'+'2').data('simwo_id');
			ajax_submit_word(event, 'similar', wo_id, null, sel_word.attr('woid'));
			_move_next_word(sel_word, e);
		}

		// '3': choose the third similar word
		if (keypress == '51' && !_toprightInputBoxes_have_focus()){ 
			var wo_id = $('.kb_short_'+'3').data('simwo_id');
			ajax_submit_word(event, 'similar', wo_id, null, sel_word.attr('woid'));
			_move_next_word(sel_word, e);
		}

		// '4': choose the fourth similar word
		if (keypress == '52' && !_toprightInputBoxes_have_focus()){ 
			var wo_id = $('.kb_short_'+'4').data('simwo_id');
			ajax_submit_word(event, 'similar', wo_id, null, sel_word.attr('woid'));
			_move_next_word(sel_word, e);
		}

		// '5': choose the fifth similar word
		if (keypress == '53' && !_toprightInputBoxes_have_focus()){ 
			var wo_id = $('.kb_short_'+'5').data('simwo_id');
			ajax_submit_word(event, 'similar', wo_id, null, sel_word.attr('woid'));
			_move_next_word(sel_word, e);
		}

		// 'altGr+w': submit the form to save the word´s definition
		if (keypress == '229'){ 
			$('#submit_word').trigger('click');
			event.preventDefault();
			_move_next_word(sel_word, e);
		}
	});
});



