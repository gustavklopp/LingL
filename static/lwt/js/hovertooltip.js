//     Hovering on a word of the text inside text_read trigger a little tooltip                  //         
/* HOVERING */
// the tooltip displayed when hovering over words in text_read

function create_tooltip_title(chosen_symbol, trans,roman,status) {
	/* called by updating the hovering tooltip. 
	either for a word => presymbol: ▶   
	either for a compountword => presymbol: • */
	var ret = '\x0d'; // line return
	var r = '';
	var symbol;
	if (chosen_symbol == 'word_symbol'){
		symbol = '▶ ';
	} else if (chosen_symbol == 'coword_symbol'){
		symbol = '• ';
	}
	if (roman != 'None' && roman != '' && roman != null && roman != 'NULL') { 
		r += ret  + '(' + roman + ')';}
	if (trans != 'None' && trans != '' && trans != null && trans != 'NULL') { 
		r += ret  + symbol + trans; }
	r += ret + symbol + getStatusName(status) + ' [' + getStatusAbbr(status) + ']';
	return r;
}

/* Helper functions for create_tooltip_title */
function getStatusName(status) {
	/* Display the tooltip when hovering (not clicked) over words in text_read -> Blablabla Unknown[?] */
	var stat = STATUSES[status];
	if (stat === undefined || stat == '1') { // Learning status can be between 1 and 99, so no defined as a constant
		return 'Learning';
		} else {
		return STATUSES[status]['name'];
	} 
}

function getStatusAbbr(status) {
	/* Display the tooltip when hovering (not clicked) over words in text_read -> Blablabla Unknown[?] */
	var stat = STATUSES[status];
	if (stat === undefined || stat == '1') { // Learning status can be between 1 and 99, so no defined as a constant
		return status;
		} else {
		return STATUSES[status]['abbr'];
	} 
}