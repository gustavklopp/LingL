function clickword(event) { // check whether a word is clicked (and +ctrl-clicked)
	// change the color when clicked depending on a click or Ctrl-click event:
	if (event.ctrlKey){
		$(this).addClass('ctrlclicked');
	} else {
		$('.clicked').removeClass('clicked'); // only one word can be clicked at one time
		$('.ctrlclicked').removeClass('ctrlclicked'); 
		$('.firstword').removeClass('firstword'); 
		$(this).addClass('clicked');
		// reset the global variables needed for storing compound words:
		compoundword_id_list = []; 
		dictwebpage_searched_word = []; 
	}
	// global variables need updating
	compoundword_id_list.push(parseInt($(this).attr('woid'))); 
	dictwebpage_searched_word.push($(this).attr('wowordtext')); 

	//click_ctrlclick_toggle func is defined in its own file (with the same name in lwt/js)
	click_ctrlclick_toggle(this, event); // creating: clicktooltip and the right panel (bottom & top)
	// and if status == 0: the termform at the top right, and the dictwebpage at the bottom right
};

function _str_to_bool(boolstr){
	if (boolstr == 'True' || boolstr == 'true'){
		return true;
	} else {
		return false;
	}
}

/* creating: clicktooltip, the termform at the top right, and the dictwebpage at the bottom right 
   -when clicling in text_read (simple click)
   -when control+clicking another time in text_read  
   -when toggling the 'show compound word' in the tooltip */
function click_ctrlclick_toggle(el, event, op=null) {
	if (el instanceof jQuery){ //it's already a Jquery obj (if the event is a 'keyboard moving shortcut')
		var $el = el;
	} else { //convert to Jquery obj (if the event is a 'click on word')
		var $el = $(el);
	}

	
	var toggle_show_compoundword = '';

	//	called by clicking on a word
	var click = event;

	if (click.ctrlKey){ // function is called by control+clicking on a word
		//compoundword_id_list.push(parseInt($el.attr('woid'))); // add the word already in termform to the already
																  // knwon compoundword
		ajax_ctrlclicked_compoundword(compoundword_id_list, 'new', RTL); // display the termform
		return false; // don't continue after it: Don't open a tooltip 
	}

	var $el_show_compoundword = _str_to_bool($el.attr('show_compoundword'));
	var $el_iscompoundword = _str_to_bool($el.attr('iscompoundword'));
	if ($el_show_compoundword){
		var status = $el.attr('cowostatus');
		var wordtext = $el.attr('cowordtext');
		var translation = $el.attr('cowotranslation');
	} else {
		var status = $el.attr('wostatus');
		var wordtext = $el.attr('wordtext');
		var translation = $el.attr('wotranslation');
	}


	if ( status == 0 ) { // word is Unknown (status 0)
		// change only the text inside the tooltip if the event is a toggle show_compoundword
		// or if the tooltip must only be updated
		if (typeof event == "boolean" && op=='update_tooltip'){ 
			var $event_show_compoundword = event;
			if($event_show_compoundword){
				$('#'+ $el.attr('woid') + '.tooltip').text(
					text_tooltip_stat_unkwn(WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('cowowordtext'), 
					$el.attr('cowotranslation'), status, $el.attr('cowotranslation'),$el_iscompoundword, 
					$event_show_compoundword, RTL )); 
			} else {
				$('#'+ $el.attr('woid') + '.tooltip').text(
					text_tooltip_stat_unkwn(WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('wowordtext'), 
					$el.attr('wotranslation'), status, $el.attr('cowotranslation'),$el_iscompoundword, 
					$event_show_compoundword, RTL )); 
			}
		} else {
			create_tooltip_stat_unkwn (WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('wowordtext'), 
				$el.attr('wotranslation'), status, $el.attr('cowotranslation'),$el_iscompoundword, 
				$el_show_compoundword, RTL ); 
		}	
			// create AJAX inside the top right of text_read with the form termform
			// get the words also by the return in function to be searched inside dictwebpage:
			// we abort the previous AJAX if needed:
			if(typeof $ajaxClickedWord !== 'undefined'){
				$ajaxClickedWord.abort();
			}
			$ajaxClickedWord = ajax_clicked_word($el.attr('woid'), $el_show_compoundword, 'new', RTL);

			// sends by AJAX data to refresh the bottom right of text_read with the dict webpage inside
			// ajax_dictwebpage(WBLINK1, dictwebpage_searched_word);
			//ajax_dictwebpage(WBLINK1, $el.attr('wowordtext'));
	}
	else if ( status == 100 ) {// word is well-known
		// change only the text inside the tooltip if the event is a toggle show_compoundword
		// or if the tooltip must only be updated
		if (typeof event == "boolean" && op=='update_tooltip'){ 
			var $event_show_compoundword = event;
			r = text_tooltip_stat_wellkwn(WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('wowordtext'), 
				$el.attr('wotranslation'), status, $el.attr('cowordtext'), $el.attr('cowotranslation'),
				$el.attr('cowostatus'), $el_iscompoundword, $event_show_compoundword, $el.attr('cowo_id_list'),  RTL ) 
//			$('#'+ $el.attr('woid') + '.tooltip').text(r);  
			$('#overlibDiv .tooltiptext').parent().replaceWith(r); 
			ajax_toggle_show_compoundword($el.attr('woid'), $event_show_compoundword);
		} else {
			create_tooltip_stat_wellkwn(WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('wowordtext'), 
				$el.attr('wotranslation'), status, $el.attr('cowordtext'), $el.attr('cowotranslation'),
				$el.attr('cowostatus'), $el_iscompoundword, $el_show_compoundword, $el.attr('cowo_id_list'),  RTL ); 
		}
	}
	else if ( status == 101 ) {// word is ignored 
		// change only the text inside the tooltip if the event is a toggle show_compoundword
		// or if the tooltip must only be updated
		if (typeof event == "boolean" && op=='update_tooltip'){ 
			var $event_show_compoundword = event;
			$('#'+ $el.attr('woid') + '.tooltip').text(
			text_tooltip_stat_ignored(WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('wowordtext'), 
			$el.attr('wotranslation'), status, $el.attr('cowotranslation'),$el_iscompoundword, 
			$event_show_compoundword, RTL )); 
		} else {
		create_tooltip_stat_ignored(WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('wowordtext'), 
			$el.attr('wotranslation'), status, $el.attr('cowotranslation'),$el_iscompoundword, 
			$el_show_compoundword, RTL ); 
		}
	}
	else {// status is 'learning')
		// change only the text inside the tooltip if the event is a toggle show_compoundword
		// or if the tooltip must only be updated
		if (typeof event == "boolean" && op=='update_tooltip'){ 
			var $event_show_compoundword = event;
			r = text_tooltip_stat_learning(WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('wowordtext'), 
				$el.attr('wotranslation'), status, $el.attr('cowordtext'), $el.attr('cowotranslation'),
				$el.attr('cowostatus'), $el_iscompoundword, $event_show_compoundword, $el.attr('cowo_id_list'),  RTL ) 
//			$('#'+ $el.attr('woid') + '.tooltip').text(r);  
			$('#overlibDiv .tooltiptext').parent().replaceWith(r); 
			ajax_toggle_show_compoundword($el.attr('woid'), $event_show_compoundword);
		} else {
			create_tooltip_stat_learning(WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('wowordtext'), 
				$el.attr('wotranslation'), status, $el.attr('cowordtext'), $el.attr('cowotranslation'),
				$el.attr('cowostatus'), $el_iscompoundword, $el_show_compoundword, $el.attr('cowo_id_list'), RTL ); 
		}
	}
	return false;
}