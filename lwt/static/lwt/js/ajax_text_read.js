$(document).ready( function(e) { 
	// make sure that a word is selected at the start (else the shortcuts can't work) 
	// (just before the first unknown word, except if it´s the first of the text) 
	//select the word before the first unknown word as the start
	//it´s an unknown word: (but if compound word and showing it, continue)

	// global variable (used especially for ajax_webpage_read.js in fact)
	var DOCUMENT =  $(document);	
	window.DOCUMENT = DOCUMENT;
	var sel_word = $('#thetext span[wostatus="0"]:not([show_compoundword="True"][cowostatus!="0"])').first(); 
	initialize_to_selectedword(sel_word, e);

	//Bind the keys event
	key_binding(e);

	$('span[woid]').each(function() { // display the hovering tooltip 
		
		update_title($(this), $(this).attr('iscompoundword'), $(this).attr('wowordtext'), 
				$(this).attr('wotranslation'), $(this).attr('woromanization'), $(this).attr('wostatus'), 
				$(this).attr('cowordtext'), $(this).attr('cowotranslation'), $(this).attr('coworomanization'), 
				$(this).attr('cowostatus'), $(this).attr('show_compoundword'));

		});

	$('span[woid]').bind('click', clickword);
	
	update_workcount(); 
});

