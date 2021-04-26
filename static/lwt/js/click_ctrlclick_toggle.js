function clickword(event) { // check whether a word is clicked (and +ctrl-clicked)
	//click_ctrlclick_toggle func is defined in its own file (with the same name in lwt/js)
	click_ctrlclick_toggle(this, event); // creating: clicktooltip and the right panel (bottom & top)
	// and if status == 0: the termform at the top right, and the dictwebpage at the bottom right
	
	// change the color when clicked:
	if (event.ctrlKey){
		$(this).addClass('ctrlclicked');
	} else {
		$('.clicked').removeClass('clicked'); // only one word can be clicked at one time
		$('.ctrlclicked').removeClass('ctrlclicked'); 
		$(this).addClass('clicked');
	}
};

/* creating: clicktooltip, the termform at the top right, and the dictwebpage at the bottom right 
   -when clicling in text_read (simple click)
   -when control+clicking another time in text_read  
   -when toggling the 'show compound word' in the tooltip */
function click_ctrlclick_toggle(el, event) {

	if (el instanceof jQuery){ //it's already a Jquery obj (if the event is a 'keyboard moving shortcut')
		var $el = el;
	} else { //convert to Jquery obj (if the event is a 'click on word')
		var $el = $(el);
	}

	var toggle_show_compoundword = '';
	
	if (event instanceof $.Event){ // function is called by clicking on a word
		var click = event;

		if (click.ctrlKey){ // function is called by control+clicking on a word
			compoundword_id_list.push(parseInt($el.attr('woid'))); // add the word already in termform to the already
			                                                          // knwon compoundword
			ajax_ctrlclicked_compoundword(compoundword_id_list, 'new', RTL); // display the termform
			return false; // don't continue after it: Don't open a tooltip 
			} 
	/* NOT USED finally
	} else { // function is called by toggling 'show_compoundword' in ClickTooltip
		toggle_show_compoundword = event;
		// remove Clicked tooltip already created
		ajax_update_DB_show_compoundword($el.attr('woid'), toggle_show_compoundword);
		*/
	}

	var show_compoundword = $el.attr('show_compoundword');
	if (show_compoundword == 'true' || show_compoundword == 'True'){
		var status = $el.attr('cowostatus');
	} else {
		var status = $el.attr('wostatus');
	}

	if ( status == 0 ) { // word is Unknown (status 0)
		if (event == toggle_show_compoundword){ // change only the text inside the tooltip if the event is a toggle show_compoundword
			$('#'+ $el.attr('woid') + '.tooltip').text(
			text_tooltip_stat_unkwn(WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('wowordtext'), $el.attr('wotranslation'),
				status, $el.attr('cowotranslation'),$el.attr('iscompoundword'), $el.attr('show_compoundword'), RTL )); 
		} else {
			create_tooltip_stat_unkwn (WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('wowordtext'), $el.attr('wotranslation'),
				status, $el.attr('cowotranslation'),$el.attr('iscompoundword'), $el.attr('show_compoundword'), RTL ); 
		}	
			// create AJAX inside the top right of text_read with the form termform
			// get the words also by the return in function to be searched inside dictwebpage:
			ajax_clicked_word($el.attr('woid'), $el.attr('show_compoundword'), 'new', RTL);
			// sends by AJAX data to refresh the bottom right of text_read with the dict webpage inside
			// ajax_dictwebpage(WBLINK1, dictwebpage_searched_word);
			//ajax_dictwebpage(WBLINK1, $el.attr('wowordtext'));
	}
	else if ( status == 100 ) {// word is well-known
		if (event == toggle_show_compoundword){ // change only the text inside the tooltip if the event is a toggle show_compoundword
			$('#'+ $el.attr('woid') + '.tooltip').text(
			text_tooltip_stat_wellkwn(WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('wowordtext'), $el.attr('wotranslation'),
				status, $el.attr('cowotranslation'),$el.attr('iscompoundword'), $el.attr('show_compoundword'), RTL )); 
		} else {
		create_tooltip_stat_wellkwn(WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('wowordtext'), $el.attr('wotranslation'),
				status, $el.attr('cowotranslation'),$el.attr('iscompoundword'), $el.attr('show_compoundword'), RTL ); 
		}
	}
	else if ( status == 101 ) {// word is ignored 
		if (event == toggle_show_compoundword){ // change only the text inside the tooltip if the event is a toggle show_compoundword
			$('#'+ $el.attr('woid') + '.tooltip').text(
			text_tooltip_stat_ignored(WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('wowordtext'), $el.attr('wotranslation'),
				status, $el.attr('cowotranslation'),$el.attr('iscompoundword'), $el.attr('show_compoundword'), RTL )); 
		} else {
		create_tooltip_stat_ignored(WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('wowordtext'), $el.attr('wotranslation'),
				status, $el.attr('cowotranslation'),$el.attr('iscompoundword'), $el.attr('show_compoundword'),RTL ); 
		}
	}
	else {// status is 'learning')
		if (event == toggle_show_compoundword){ // change only the text inside the tooltip if the event is a toggle show_compoundword
			$('#'+ $el.attr('woid') + '.tooltip').text(
			text_tooltip_stat_learning(WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('wowordtext'), $el.attr('wotranslation'),
				status, $el.attr('cowotranslation'),$el.attr('iscompoundword'), $el.attr('show_compoundword'), RTL )); 
		} else {
		create_tooltip_stat_learning(WBLINK1,WBLINK2,WBLINK3, $el.attr('woid'), $el.attr('wowordtext'), $el.attr('wotranslation'), 
				status, $el.attr('cowotranslation'),$el.attr('iscompoundword'), $el.attr('show_compoundword'),RTL ); 
		}
	}
	return false;
}