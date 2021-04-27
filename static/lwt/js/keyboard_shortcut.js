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
	$( "#bottomleft" ).bind( "click", function(e) {
		  $( this ).focus();
		e.preventDefault();
	});
	//case where we open a brand new text. The word selected will be a unknown word
	// therefore, make it like I click on it.
	if (sel_word.attr('wostatus') == 0){
		click_ctrlclick_toggle(sel_word, e); // creating: clicktooltip and the right panel (bottom & top)
	}
	// give the focus to the text since it allows to use the keyboard shorcuts
	$("#bottomleft").focus();
});


$(function() {

	$(window).keydown(function(e) { // only keydown is able to get the arrow keys... (strange)
		//the current selected word:
		var sel_word = $('.clicked');

		var ev = e || window.event;
		var keydown = ev.keyCode || ev.which;
		//do stuff with "key" here...
		if (keydown == '39' && $("#bottomleft").is(":focus")){ // arrow right
			sel_word.removeClass('clicked'); //unselect the current word
			var next_word = sel_word.next();
			while(_is_in_text(next_word)){
				if (_is_word(next_word)){
					sel_word = next_word;
					break;
				} else {
					next_word = next_word.next()
				}
			}
			sel_word.addClass('clicked'); //select the next word
			click_ctrlclick_toggle(sel_word, e); // creating: clicktooltip and the right panel (bottom & top)
		}
		if (keydown == '37' && $("#bottomleft").is(":focus")){ // arrow left
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
				
		if (keypress == '97' && $("#bottomleft").is(":focus")){ // 'a': I know this term well
			ajax_update_status(sel_word.attr('woid'), 'wellkwn');
		}
		
		if (keypress == '115' && $("#bottomleft").is(":focus")){ // 's': Ignore this term
			ajax_update_status(sel_word.attr('woid'), 'ignored');
		}
		
		if (keypress == '100' && $("#bottomleft").is(":focus")){ // 'd': link dict1
			ajax_dictwebpage(WBLINK1, sel_word.attr('wowordtext'),'');
		}
		
		if (keypress == '68' && $("#bottomleft").is(":focus")){ // 'D': link dict2
			ajax_dictwebpage(WBLINK2, sel_word.attr('wowordtext'),'');
		}
		
		if (keypress == '103' && $("#bottomleft").is(":focus")){ // 'g': link gogle word
			ajax_dictwebpage(WBLINK3, sel_word.attr('wowordtext'),'');
		}
		
		if (keypress == '71' && $("#bottomleft").is(":focus")){ // 'G': link google sentence
			ajax_dictwebpage(WBLINK3, sel_word.attr('wowordtext'), sel_word.attr('woid'));
		}
		
		if (keypress == '116' && $("#bottomleft").is(":focus")){ // 't': focus on translate input box
			$('#id_translation').focus();
		}
		
		if (keypress == '49' && $("#bottomleft").is(":focus")){ // '1': choose the first similar word
			var wo_id = $('.kb_short_'+'1').data('simwo_id');
			ajax_submit_word('similar', wo_id, sel_word.attr('woid'));
		}
		if (keypress == '50' && $("#bottomleft").is(":focus")){ // '2': choose the second similar word
			var wo_id = $('.kb_short_'+'2').data('simwo_id');
			ajax_submit_word('similar', wo_id, sel_word.attr('woid'));
		}
		if (keypress == '51' && $("#bottomleft").is(":focus")){ // '3': choose the third similar word
			var wo_id = $('.kb_short_'+'3').data('simwo_id');
			ajax_submit_word('similar', wo_id, sel_word.attr('woid'));
		}
		if (keypress == '52' && $("#bottomleft").is(":focus")){ // '4': choose the fourth similar word
			var wo_id = $('.kb_short_'+'4').data('simwo_id');
			ajax_submit_word('similar', wo_id, sel_word.attr('woid'));
		}
		if (keypress == '53' && $("#bottomleft").is(":focus")){ // '5': choose the fifth similar word
			var wo_id = $('.kb_short_'+'5').data('simwo_id');
			ajax_submit_word('similar', wo_id, sel_word.attr('woid'));
		}

		if (keypress == '229' && $("textarea#id_translation").is(":focus")){ // 'altGr+w': submit the form to save the word´s definition
			$('#submit_word').trigger('click');
		}
	});
});



