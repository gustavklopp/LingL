//////////////////////////////////////////////////////////////////////////////////////////////////
//     creating the links inside the tooltip (when clicking on word in text_read)               //
//////////////////////////////////////////////////////////////////////////////////////////////////

/**************************************************************
 called by 
create_tooltip_stat_unkwn(WBLINK1,WBLINK2,WBLINK3,$(this).attr('wotranslation'), $(this).attr('wowordtext'), RTL, $(this).attr('woid'), status); 
     wblink1: language.dict1uri
     wblink2: language.dict2uri
     wblink3: language.lggoogletranslateuri
***************************************************************/

function text_tooltip_stat_unkwn(wblink1,wblink2,wblink3, wo_id, wowordtext, trans, wostatus, cotrans, iscompoundword, show_compoundword, rtl)
{
	r =
		'<div class="tooltiptext" id="'+wo_id+'">' +
		'<b>' + escape_html_chars(wowordtext) + '</b><br>' +
		show_compoundword_checkbox(wo_id, iscompoundword, show_compoundword) +
		create_link_stat_wellkwn(wo_id) + ' <br> ' + // "I know this term well" 
		create_link_stat_ignored(wo_id) + ' <br> ' + // "Ignore this term" 
		create_links_webdict(wblink1,wblink2,wblink3,wowordtext,wo_id) +
		'</div>';
	return r;
}

function text_tooltip_stat_learning(wblink1,wblink2,wblink3, wo_id, wowordtext, trans, wostatus, cotrans, iscompoundword, show_compoundword, rtl)
{
	r =
		'<div class="tooltiptext" id="'+wo_id+'">' +
		'<b>' + escape_html_chars(wowordtext) + '</b><br>' +
		show_compoundword_checkbox(wo_id, iscompoundword, show_compoundword) +
		check_undefined_else_return(trans) + // display translation if any
		create_link_editword(wo_id,wowordtext,wblink1) +' | '+ create_link_deleteword(wo_id) + ' <br> ' + // "Edit term | delete term"
		create_link_deletesingleword(wo_id) + '<br>'+ // delete only the word, not the similar words with it
		create_links_webdict(wblink1,wblink2,wblink3,wowordtext,wo_id) +
		'</div>' ;
	return r;
}
function text_tooltip_stat_ignored(wblink1,wblink2,wblink3, wo_id, wowordtext, trans, wostatus, cotrans, iscompoundword, show_compoundword, rtl)
{
	r =
		'<div class="tooltiptext" id="'+wo_id+'">' +
		'<b>' + escape_html_chars(wowordtext) + '</b><br>' +
		show_compoundword_checkbox(wo_id, iscompoundword, show_compoundword) +
		check_undefined_else_return(trans) +
		create_link_editword(wo_id,wowordtext,wblink1) + ' | ' + create_link_deleteword(wo_id) + ' <br> ' +
		create_link_deletesingleword(wo_id) + '<br>'+ // delete only the word, not the similar words with it
		create_links_webdict(wblink1,wblink2,wblink3,wowordtext,wo_id) +
		'</div>' ;
	return r;
}

function text_tooltip_stat_wellkwn(wblink1,wblink2,wblink3, wo_id, wowordtext, trans, wostatus, cotrans, iscompoundword, show_compoundword, rtl)
{
	r =
		'<div class="tooltiptext" id="'+wo_id+'">' +
		'<b>' + escape_html_chars(wowordtext) + '</b><br>' +
		show_compoundword_checkbox(wo_id, iscompoundword, show_compoundword) +
		check_undefined_else_return(trans) +
		create_link_editword(wo_id,wowordtext,wblink1) + ' | ' + create_link_deleteword(wo_id) + ' <br> ' +
		create_link_deletesingleword(wo_id) + '<br>'+ // delete only the word, not the similar words with it
		create_links_webdict(wblink1,wblink2,wblink3,wowordtext,wo_id) +
		'</div>' ;
	return r;
}
/* the user clicked on a WORD 
 the word can be of the status: ignored, well-known, learning, unknown. */
function create_tooltip_stat_unkwn(wblink1,wblink2,wblink3, wo_id, wowordtext, trans, wostatus, 
		cotrans, iscompoundword, show_compoundword, rtl)
{
	return overlib(
		text_tooltip_stat_unkwn(wblink1,wblink2,wblink3, wo_id, wowordtext, trans, wostatus, 
				cotrans, iscompoundword, show_compoundword, rtl),
		CAPTION, 'New Word');                                                // "Loolup Sentence: GTr"        
}

function create_tooltip_stat_learning(wblink1,wblink2,wblink3, wo_id, wowordtext, trans, wostatus, 
		cotrans, iscompoundword, show_compoundword, rtl)
{
	return overlib(
		text_tooltip_stat_learning(wblink1,wblink2,wblink3, wo_id, wowordtext, trans, wostatus, 
				cotrans, iscompoundword, show_compoundword, rtl),
		CAPTION, 'Learning');
}
function create_tooltip_stat_ignored(wblink1,wblink2,wblink3, wo_id, wowordtext, trans, wostatus, 
		cotrans, iscompoundword, show_compoundword, rtl)
{
	return overlib(
		text_tooltip_stat_ignored(wblink1,wblink2,wblink3, wo_id, wowordtext, trans, wostatus, 
				cotrans, iscompoundword, show_compoundword, rtl),
		CAPTION, 'ignored');
}

function create_tooltip_stat_wellkwn(wblink1,wblink2,wblink3, wo_id, wowordtext, trans, wostatus, 
		cotrans, iscompoundword, show_compoundword, rtl)
{
	return overlib(
		text_tooltip_stat_wellkwn(wblink1,wblink2,wblink3, wo_id, wowordtext, trans, wostatus, 
				cotrans, iscompoundword, show_compoundword, rtl),
		CAPTION, 'Well-known');
}

/**************************************************************
 		HELPER FUNCTIONS:
 Called inside the functions above: for ex. in : 
 		"create_link_stat_wellkwn(txid,torder) + ' <br> ' +  
 		"create_link_stat_ignored(txid,torder) + 
 		"create_links_webdict(wblink1,wblink2,wblink3,txt,txid,torder), => create the link to the dictionary webpage 
***************************************************************/

function show_compoundword_checkbox(wo_id, iscompoundword, show_compoundword){
		/* display a checkbox for showing compoundword:*/
		var r = '';
		if (iscompoundword == 'true' || iscompoundword == 'True') {
			r += '<input type="checkbox" name="show_compoundword_checkbox" onchange="';
			r += 'click_ctrlclick_toggle($(\'span[woid='+wo_id+']\'),this.checked)"';

			if (show_compoundword == 'True'){
				r += ' checked';
			}
			r += '>show compoundword?<br>'; 
		}
		return r;
}


function check_undefined_else_return(myvar){
		/* check if the var has beed defined, then return it if yes:*/
		if (typeof myvar != 'undefined' && myvar != '' && myvar != 'None'){
			r = '<b>▶ ' + escape_html_chars(myvar) + '</b><br> ' ;
		} else { r = '';}
		return r;
}

/* create: "Lookup Term: <a hrf="linktodict1">Dict1</a> <a hrf="linktodict2">Dict2</a> <a hrf="linktodGtr">Gtr</a>
 		   "Lookup Sentence: <a hrf="linktoGtr>Gtr</a>" */
function create_links_webdict(wblink1,wblink2,wblink3,wowordtext,wo_id) {
	var s =  
	create_link_webdict(wblink1,wowordtext,'Dict1','Lookup Term: ') + 
	create_link_webdict(wblink2,wowordtext,'Dict2','') +
	create_link_webdict(wblink3,wowordtext,'GTr','') + 
	// search also for sentence in lggoogletranslate (wblink3)
	'<br>Lookup Sentence: ' + createSentLookupLink(wblink3,'GTr',wo_id);
	return s;
}


function create_link_newword(wo_id,wowordtext,wblink1) {
	return ' <a href="" onClick="ajax_termform(\''+wo_id+'\',\'new\',\'\');ajax_dictwebpage(\''+wblink1+'\',\''+wowordtext+'\');return false;">New term</a> ';
}


function create_link_editword(wo_id, wowordtext, wblink1) {
	return ' <a href="" onClick="ajax_termform(\''+wo_id+'\',\'edit\',\'\');ajax_dictwebpage(\''+wblink1+'\',\''+wowordtext+'\');return false;">Edit term</a> ';
}

/* NOT USED YET */
function create_link_editword_title(text,txid,torder,wid) {
	return '<a style=\x22color:yellow\x22 href=\x22edit_word.php?tid=' + 
		txid + '&amp;ord=' + torder + 
		'&amp;wid=' + wid + '\x22 target=\x22ro\x22>' + text + '</a>';
}

function create_link_deleteword(wo_id) {
	return ' <a href="" onClick="ajax_del_word(\''+wo_id+'\');return false;">Delete term</a> ';
}

function create_link_deletesingleword(wo_id) {
	return ' <a href="" onClick="ajax_del_singleword(\''+wo_id+'\');return false;">Delete single term</a> ';
}

function create_link_stat_wellkwn(wo_id) {
	return ' <a href="" onClick="ajax_update_status(\''+wo_id+'\',\'wellkwn\');return false;">I know this term well</a> ';
}

function create_link_stat_ignored(wo_id) {
	return ' <a href="" onClick="ajax_update_status(\''+wo_id+'\',\'ignored\');return false;">Ignore this term</a> ';
}

/**************************************************************
String extensions
***************************************************************/

String.prototype.rtrim = function () {
  return this.replace (/\s+$/, '');
}

String.prototype.ltrim = function () {
  return this.replace (/^\s+/, '');
}

String.prototype.trim = function (clist) {
  return this.ltrim().rtrim();
};

/**************************************************************
Other JS utility functions
***************************************************************/

// open the webpage dictionary at the bottom right of text_read and search sentence
function translateSentence(url,sentctl) {
	if ((typeof sentctl != 'undefined') && (url != '')) {
		text = sentctl.value;
		if (typeof text == 'string') {
			// create AJAX inside the bottom right of text_read 
			$.ajax({url: '/webdicturi/',
								type: 'GET',
								data: {'finalurl': createTheDictUrl(url,text.replace(/[{}]/g, ''))},
								success: function(data){ $('#bottomright.text_read').html(data); }
								})
			//window.parent.frames['ru'].location.href = 
			//createTheDictUrl(url,text.replace(/[{}]/g, ''));
		}
	}
}

function translateSentence2(url,sentctl) {
	if ((typeof sentctl != 'undefined') && (url != '')) {
		text = sentctl.value;
		if (typeof text == 'string') {
			owin (	
				createTheDictUrl(url, text.replace(/[{}]/g, '') )
			);
		}
	}
}

// open the webpage dictionary at the bottom right of text_read and search word
function translateWord(url,wordctl) {
	if ((typeof wordctl != 'undefined') && (url != '')) {
		text = wordctl.value;
		if (typeof text == 'string') {
			// create AJAX inside the bottom right of text_read 
			$.ajax({url: '/webdicturi/',
								type: 'GET',
								data: {'finalurl': createTheDictUrl(url, text)},
								success: function(data){ $('#bottomright.text_read').html(data); }
								})
			//window.parent.frames['ru'].location.href = 
			//	createTheDictUrl(url, text);
		}
	}
}

function translateWord2(url,wordctl) {
	if ((typeof wordctl != 'undefined') && (url != '')) {
		text = wordctl.value;
		if (typeof text == 'string') {
			owin ( createTheDictUrl(url, text) );
		}
	}
}

function translateWord3(url,word) {
	owin ( createTheDictUrl(url, word) );
}



function createTheDictUrl(u,w) {
	var url = u.trim();
	var trm = w.trim();
	var r = 'dictwebpage?x=2&i=' + escape(u) + '&t=' + w;
	return r;
}

// create the link after "Lookup Term" in the tooltip (link to dictionary 1, 2, and GTr)
function create_link_webdict(u,w,t,b) {
	var url = u.trim();
	var trm = w.trim();
	var txt = t.trim();
	var txtbefore = b.trim();
	var issentence = '';
	var r = '';
	if (url != '' && txt != '') {
			r = ' ' + txtbefore + 
	' <a  id="lookupterm_in_'+txt+'" href="" onClick="ajax_dictwebpage(\''+ url+'\',\''+ trm+'\','+issentence+'); return false;">' + txt + '</a> ';
	}
	return r;
}

// create the link after "Lookup sentence" in the tooltip
function createSentLookupLink(url,txt,wo_id) {
	var searchedword = ''; // we'll look for the complete sentence, not a word
	var url = url.trim();
	var txt = txt.trim();
	var issentence = wo_id;
	var r = '';
	if (url != '' && txt != '') {
	r = ' <a id="lookupterm_in_'+txt+'" href="" onClick="ajax_dictwebpage(\''+url+'\',\''+searchedword+'\',\''+issentence+'\');return false;">' + txt + '</a> ';
	}
	return r;
}

function escape_html_chars(s)
{
	return s.replace(/&/g,'%AMP%').replace(/</g,'&#060;').replace(/>/g,'&#062;').replace(/"/g,'&#034;').replace(/'/g,'&#039;').replace(/%AMP%/g,'&#038;').replace(/\x0d/g,'<br>');
}

function escape_apostrophes(s)
{
	return s.replace(/'/g,'\\\'');
}

