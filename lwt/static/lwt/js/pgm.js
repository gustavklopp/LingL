/**************************************************************
"Learning with Texts" (LWT) is free and unencumbered software 
released into the PUBLIC DOMAIN.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a
compiled binary, for any purpose, commercial or non-commercial,
and by any means.

In jurisdictions that recognize copyright laws, the author or
authors of this software dedicate any and all copyright
interest in the software to the public domain. We make this
dedication for the benefit of the public at large and to the 
detriment of our heirs and successors. We intend this 
dedication to be an overt act of relinquishment in perpetuity
of all present and future rights to this software under
copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE 
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
THE SOFTWARE.

For more information, please refer to [http://unlicense.org/].
***************************************************************/
 
/**************************************************************
LWT Javascript functions
***************************************************************/

/**************************************************************
Global variables for OVERLIB
***************************************************************/

var ol_textfont = '"Lucida Grande",Arial,sans-serif,STHeiti,"Arial Unicode MS",MingLiu';
var ol_textsize = 3;
var ol_sticky = 1;
var ol_captionfont = '"Lucida Grande",Arial,sans-serif,STHeiti,"Arial Unicode MS",MingLiu';
var ol_captionsize = 3;
var ol_width = 260;
var ol_close = 'Close';
var ol_offsety = 30;
var ol_offsetx = 3;
var ol_fgcolor = '#FFFFE8';
var ol_closecolor = '#FFFFFF';

/**************************************************************
Helper functions for overlib
***************************************************************/

function run_overlib_status_98(wblink1,wblink2,wblink3,hints,txid,torder,txt,wid,mw2,mw3,mw4,mw5,mw6,mw7,mw8,mw9,rtl,ann)
{
	return overlib(
		'<b>' + escape_html_chars_2(hints,ann) + '</b><br /> ' +
		make_overlib_link_new_word(txid,torder,wid) + ' | ' +
		make_overlib_link_delete_word(txid,wid) + 
		make_overlib_link_new_multiword(txid,torder,mw2,mw3,mw4,mw5,mw6,mw7,mw8,mw9,rtl) + ' <br /> ' +
		make_overlib_link_wb(wblink1,wblink2,wblink3,txt,txid,torder), 
		CAPTION, 'Word');
}

function run_overlib_status_99(wblink1,wblink2,wblink3,hints,txid,torder,txt,wid,mw2,mw3,mw4,mw5,mw6,mw7,mw8,mw9,rtl,ann)
{
	return overlib(
		'<b>' + escape_html_chars_2(hints,ann) + '</b><br /> ' +
		make_overlib_link_new_word(txid,torder,wid) + ' | ' +
		make_overlib_link_delete_word(txid,wid) + 
		make_overlib_link_new_multiword(txid,torder,mw2,mw3,mw4,mw5,mw6,mw7,mw8,mw9,rtl) + ' <br /> ' +
		make_overlib_link_wb(wblink1,wblink2,wblink3,txt,txid,torder), 
		CAPTION, 'Word');
}

function run_overlib_status_1_to_5(wblink1,wblink2,wblink3,hints,txid,torder,txt,wid,stat,mw2,mw3,mw4,mw5,mw6,mw7,mw8,mw9,rtl,ann)
{
	return overlib(
		'<b>' + escape_html_chars_2(hints,ann) + '</b><br /> ' +
		make_overlib_link_change_status_all(txid,torder,wid,stat) + ' <br /> ' +
		make_overlib_link_edit_word(txid,torder,wid) + ' | ' +
		make_overlib_link_delete_word(txid,wid) + 
		make_overlib_link_new_multiword(txid,torder,mw2,mw3,mw4,mw5,
		mw6,mw7,mw8,mw9,rtl) + ' <br /> ' +
		make_overlib_link_wb(wblink1,wblink2,wblink3,txt,txid,torder),
		CAPTION, make_overlib_link_edit_word_title(
		'Word &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;',txid,torder,wid));
}

function run_overlib_status_unknown(wblink1,wblink2,wblink3,hints,txid,torder,txt,mw2,mw3,mw4,mw5,mw6,mw7,mw8,mw9,rtl)
{
	return overlib(
		'<b>' + escape_html_chars(hints) + '</b><br /> ' +
		make_overlib_link_wellknown_word(txid,torder) + ' <br /> ' +  
		make_overlib_link_ignore_word(txid,torder) + 
		make_overlib_link_new_multiword(txid,torder,mw2,mw3,mw4,mw5,mw6,mw7,mw8,mw9,rtl) + ' <br /> ' +
		make_overlib_link_wb(wblink1,wblink2,wblink3,txt,txid,torder),
		CAPTION, 'New Word');
}

function run_overlib_multiword(wblink1,wblink2,wblink3,hints,txid,torder,txt,wid,stat,wcnt,ann)
{
	return overlib(
		'<b>' + escape_html_chars_2(hints,ann) + '</b><br /> ' +
		make_overlib_link_change_status_all(txid,torder,wid,stat) + ' <br /> ' +
		make_overlib_link_edit_multiword(txid,torder,wid) + ' | ' +
		make_overlib_link_delete_multiword(txid,wid) + ' <br /> ' +
		make_overlib_link_wb(wblink1,wblink2,wblink3,txt,txid,torder),
		CAPTION, make_overlib_link_edit_multiword_title(wcnt.trim() + '-Word-Expression',txid,torder,wid));
}

function run_overlib_test(wblink1,wblink2,wblink3,wid,txt,trans,roman,stat,sent,todo,oldstat)
{
	var s = parseInt(stat,10);
	var c = s+1; 
	if(c>5) c=5; 
	var w = s-1; 
	if(w<1) w=1;
	var cc = stat + ' ▶ ' + c; if(c==s) cc=c; 
	var ww = stat + ' ▶ ' + w; if(w==s) ww=w;
	return overlib(
	(todo == 1 ?
		'<center><hr noshade size=1 /><b>' +
		((stat >= 1 && stat <=5) ? (
		make_overlib_link_change_status_test(wid,1,'<img src=\x22icn/thumb-up.png\x22 title=\x22Got it!\x22 alt=\x22Got it!\x22 /> Got it! [' + cc + ']') + 
		'<hr noshade size=1 />' +
		make_overlib_link_change_status_test(wid,-1,'<img src=\x22icn/thumb.png\x22 title=\x22Oops!\x22 alt=\x22Oops!\x22 /> Oops! [' + ww + ']') + 
		'<hr noshade size=1 />'
		) : '' ) + 
		make_overlib_link_change_status_alltest(wid,stat) +
		'</b></center><hr noshade size=1 />' : 
		'') +
	'<b>' + escape_html_chars(make_tooltip(txt,trans,roman,stat)) +	
	'</b><br />' +
	' <a href=\x22edit_tword.php?wid=' + wid + '\x22 target=\x22ro\x22>Edit term</a><br />' +
	createTheDictLink(wblink1,txt,'Dict1','Lookup Term: ') +
	createTheDictLink(wblink2,txt,'Dict2','') +
	createTheDictLink(wblink3,txt,'GTr','') + 
	createTheDictLink(wblink3,sent,'GTr','<br />Lookup Sentence:'),
	CAPTION, 'Got it?');
}

function make_overlib_link_new_multiword(txid,torder,mw2,mw3,mw4,mw5,mw6,mw7,mw8,mw9,rtl) {
	if (mw2=='' && mw3=='' && mw4=='' && mw5=='' && mw6 =='' && mw7 =='' && mw8 =='' && mw9 =='') return '';
	if (rtl) return ' <br />Expr: ' +
	(mw9 != '' ? make_overlib_link_create_edit_multiword_rtl(9,txid,torder,mw9) + ' ' : '') + 
	(mw8 != '' ? make_overlib_link_create_edit_multiword_rtl(8,txid,torder,mw8) + ' ' : '') + 
	(mw7 != '' ? make_overlib_link_create_edit_multiword_rtl(7,txid,torder,mw7) + ' ' : '') + 
	(mw6 != '' ? make_overlib_link_create_edit_multiword_rtl(6,txid,torder,mw6) + ' ' : '') + 
	(mw5 != '' ? make_overlib_link_create_edit_multiword_rtl(5,txid,torder,mw5) + ' ' : '') + 
	(mw4 != '' ? make_overlib_link_create_edit_multiword_rtl(4,txid,torder,mw4) + ' ' : '') + 
	(mw3 != '' ? make_overlib_link_create_edit_multiword_rtl(3,txid,torder,mw3) + ' ' : '') + 
	(mw2 != '' ? make_overlib_link_create_edit_multiword_rtl(2,txid,torder,mw2) : '') + ' ';
	else return ' <br />Expr: ' +
	(mw2 != '' ? make_overlib_link_create_edit_multiword(2,txid,torder,mw2) + ' ' : '') + 
	(mw3 != '' ? make_overlib_link_create_edit_multiword(3,txid,torder,mw3) + ' ' : '') + 
	(mw4 != '' ? make_overlib_link_create_edit_multiword(4,txid,torder,mw4) + ' ' : '') + 
	(mw5 != '' ? make_overlib_link_create_edit_multiword(5,txid,torder,mw5) + ' ' : '') + 
	(mw6 != '' ? make_overlib_link_create_edit_multiword(6,txid,torder,mw6) + ' ' : '') + 
	(mw7 != '' ? make_overlib_link_create_edit_multiword(7,txid,torder,mw7) + ' ' : '') + 
	(mw8 != '' ? make_overlib_link_create_edit_multiword(8,txid,torder,mw8) + ' ' : '') + 
	(mw9 != '' ? make_overlib_link_create_edit_multiword(9,txid,torder,mw9) : '') + ' ';
}

function make_overlib_link_wb(wblink1,wblink2,wblink3,txt,txid,torder) {
	var s =  
	createTheDictLink(wblink1,txt,'Dict1','Lookup Term: ') +
	createTheDictLink(wblink2,txt,'Dict2','') +
	createTheDictLink(wblink3,txt,'GTr','') + 
	((torder < 1 || txid < 1) ? '' : '<br />Lookup Sentence: ' + createSentLookupLink(torder,txid,wblink3,'GTr'));
	return s;
}

function make_overlib_link_wbnl(wblink1,wblink2,wblink3,txt,txid,torder) {
	var s =  
	createTheDictLink(wblink1,txt,'Dict1','Term: ') +
	createTheDictLink(wblink2,txt,'Dict2','') +
	createTheDictLink(wblink3,txt,'GTr','') + 
	((torder < 1 || txid < 1) ? '' : ' | Sentence: ' + createSentLookupLink(torder,txid,wblink3,'GTr'));
	return s;
}

function make_overlib_link_wbnl2(wblink1,wblink2,wblink3,txt,sent) {
	var s =  
	createTheDictLink(wblink1,txt,'Dict1','Term: ') +
	createTheDictLink(wblink2,txt,'Dict2','') +
	createTheDictLink(wblink3,txt,'GTr','') + 
	((sent == '') ? '' : createTheDictLink(wblink3,sent,'GTr',' | Sentence:'));
	return s;
}

function make_overlib_link_change_status_all(txid,torder,wid,oldstat) {
	var result = 'St: ';
	for (var newstat=1; newstat<=5; newstat++)
		result += make_overlib_link_change_status(txid,torder,wid,oldstat,newstat);
	result += make_overlib_link_change_status(txid,torder,wid,oldstat,99);
	result += make_overlib_link_change_status(txid,torder,wid,oldstat,98);
	return result; 
}

function make_overlib_link_change_status_alltest(wid,oldstat) {
	var result = '';
	for (var newstat=1; newstat<=5; newstat++)
		result += make_overlib_link_change_status_test2(wid,oldstat,newstat);
	result += make_overlib_link_change_status_test2(wid,oldstat,99);
	result += make_overlib_link_change_status_test2(wid,oldstat,98);
	return result; 
}

function make_overlib_link_change_status(txid,torder,wid,oldstat,newstat) {
	if (oldstat == newstat) {
		return '<span title=\x22' + 
			getStatusName(oldstat) + '\x22>◆</span>';
	} else {
		return ' <a href=\x22set_word_status.php?tid=' + txid + 
			'&amp;ord=' + torder + 
			'&amp;wid=' + wid +
			'&amp;status=' + newstat + '\x22 target=\x22ro\x22><span title=\x22' + 
			getStatusName(newstat) + '\x22>[' + 
			getStatusAbbr(newstat) + ']</span></a> ';
	}
}

function make_overlib_link_change_status_test2(wid,oldstat,newstat) {
	if (oldstat == newstat) {
		return ' <a href=\x22set_test_status.php?wid=' + wid +
				'&amp;status=' + newstat + '\x22 target=\x22ro\x22><span title=\x22' + 
			getStatusName(newstat) + '\x22>[◆]</span></a> ';
	} else {
		return ' <a href=\x22set_test_status.php?wid=' + wid +
				'&amp;status=' + newstat + '\x22 target=\x22ro\x22><span title=\x22' + 
			getStatusName(newstat) + '\x22>[' + 
				getStatusAbbr(newstat) + ']</span></a> ';
	}
}

function make_overlib_link_change_status_test(wid,plusminus,text) {
	return ' <a href=\x22set_test_status.php?wid=' + wid +
		'&amp;stchange=' + plusminus + '\x22 target=\x22ro\x22>' + text + '</a> ';
}

function make_overlib_link_new_word(txid,torder,wid) {
	return ' <a href=\x22edit_word.php?tid=' + txid + 
		'&amp;ord=' + torder + 
		'&amp;wid=' + wid + '\x22 target=\x22ro\x22>Learn term</a> ';
}

function make_overlib_link_edit_multiword(txid,torder,wid) {
	return ' <a href=\x22edit_mword.php?tid=' + txid + 
		'&amp;ord=' + torder + 
		'&amp;wid=' + wid + '\x22 target=\x22ro\x22>Edit term</a> ';
}

function make_overlib_link_edit_multiword_title(text,txid,torder,wid) {
	return '<a style=\x22color:yellow\x22 href=\x22edit_mword.php?tid=' + txid + 
		'&amp;ord=' + torder + 
		'&amp;wid=' + wid + '\x22 target=\x22ro\x22>' + text + '</a>';
}

function make_overlib_link_create_edit_multiword(len,txid,torder,txt) {
	return ' <a href=\x22edit_mword.php?tid=' + txid + 
		'&amp;ord=' + torder + 
		'&amp;txt=' + txt +
		'\x22 target=\x22ro\x22>' + len + '..' + escape_html_chars(txt.substr(-2).trim()) + '</a> ';
}

function make_overlib_link_create_edit_multiword_rtl(len,txid,torder,txt) {
	return ' <a dir=\x22rtl\x22 href=\x22edit_mword.php?tid=' + txid + 
		'&amp;ord=' + torder + 
		'&amp;txt=' + txt +
		'\x22 target=\x22ro\x22>' + len + '..' + escape_html_chars(txt.substr(-2).trim()) + '</a> ';
}

function make_overlib_link_edit_word(txid,torder,wid) {
	return ' <a href=\x22edit_word.php?tid=' + txid + 
		'&amp;ord=' + torder + 
		'&amp;wid=' + wid + '\x22 target=\x22ro\x22>Edit term</a> ';
}

function make_overlib_link_edit_word_title(text,txid,torder,wid) {
	return '<a style=\x22color:yellow\x22 href=\x22edit_word.php?tid=' + 
		txid + '&amp;ord=' + torder + 
		'&amp;wid=' + wid + '\x22 target=\x22ro\x22>' + text + '</a>';
}

function make_overlib_link_delete_word(txid,wid) {
	return ' <a href=\x22delete_word.php?wid=' +
		wid + '&amp;tid=' + txid + '\x22 target=\x22ro\x22>Delete term</a> ';
}

function make_overlib_link_delete_multiword(txid,wid) {
	return ' <a href=\x22delete_mword.php?wid=' +
		wid + '&amp;tid=' + txid + '\x22 target=\x22ro\x22>Delete term</a> ';
}

function make_overlib_link_wellknown_word(txid,torder) {
	return ' <a href=\x22insert_word_wellknown.php?tid=' + 
		txid + '&amp;ord=' + torder + '\x22 target=\x22ro\x22>I know this term well</a> ';
}

function make_overlib_link_ignore_word(txid,torder) {
	return ' <a href=\x22insert_word_ignore.php?tid=' + txid + 
		'&amp;ord=' + torder + '\x22 target=\x22ro\x22>Ignore this term</a> ';
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

function getStatusName(status) {
	return (STATUSES[status] ? STATUSES[status]['name'] : 'Unknown');
}

function getStatusAbbr(status) {
	return (STATUSES[status] ? STATUSES[status]['abbr'] : '?');
}

function translateSentence(url,sentctl) {
	if ((typeof sentctl != 'undefined') && (url != '')) {
		text = sentctl.value;
		if (typeof text == 'string') {
			window.parent.frames['ru'].location.href = 
			createTheDictUrl(url,text.replace(/[{}]/g, ''));
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

function translateWord(url,wordctl) {
	if ((typeof wordctl != 'undefined') && (url != '')) {
		text = wordctl.value;
		if (typeof text == 'string') {
			window.parent.frames['ru'].location.href = 
				createTheDictUrl(url, text);
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

function make_tooltip(word,trans,roman,status) {
	var nl = '\x0d';
	var title = word;
	// if (title != '' ) title = '▶ ' + title;
	if (roman != '') { 
		if (title != '' ) title += nl;
		title += '▶ ' + roman;
	}
	if (trans != '' && trans != '*') { 
		if (title != '' ) title += nl;
		title += '▶ ' + trans;
	}
	if (title != '' ) title += nl;
	title += '▶ ' + getStatusName(status) + ' [' + 
	getStatusAbbr(status) + ']';
	return title;
}

function escape_html_chars_2 (title, ann) {
	if (ann != '' ) {
		var ann2 = escape_html_chars(ann);
		return escape_html_chars(title).replace(ann2,
			'<span style="color:red">' + ann2 + '</span>');
	}
	else
		return escape_html_chars(title);
}

function owin(url) {
	window.open(
		url, 
		'dictwin', 
		'width=800, height=400, scrollbars=yes, menubar=no, resizable=yes, status=no'
	);
}

function oewin(url) {
	window.open(
		url, 
		'editwin', 
		'width=800, height=600, scrollbars=yes, menubar=no, resizable=yes, status=no'
	);
}

function createTheDictUrl(u,w) {
	var url = u.trim();
	var trm = w.trim();
	var r = 'trans.php?x=2&i=' + escape(u) + '&t=' + w;
	return r;
}

function createTheDictLink(u,w,t,b) {
	var url = u.trim();
	var trm = w.trim();
	var txt = t.trim();
	var txtbefore = b.trim();
	var r = '';
	if (url != '' && txt != '') {
		if(url.substr(0,1) == '*') {
			r = ' ' + txtbefore + 
			' <span class=\x22click\x22 onclick=\x22owin(\'' + createTheDictUrl(url.substring(1),escape_apostrophes(trm)) + '\');\x22>' + txt + '</span> ';
		} 
		else {
			r = ' ' + txtbefore + 
			' <a href=\x22' + createTheDictUrl(url,trm) + '\x22 target=\x22ru\x22>' + txt + '</a> ';
		} 
	}
	return r;
}

function createSentLookupLink(torder,txid,url,txt) {
	var url = url.trim();
	var txt = txt.trim();
	var r = '';
	if (url != '' && txt != '') {
		if((url.substr(0,8) == '*http://') || (url.substr(0,9) == '*https://')) {
			r = ' <span class=\x22click\x22 onclick=\x22owin(\'trans.php?x=1&i=' + torder + '&t=' + txid + '\');\x22>' + txt + '</span> ';
		} 
		else if ((url.substr(0,7) == 'http://') || (url.substr(0,8) == 'https://')) {
			r = ' <a href=\x22trans.php?x=1&i=' + torder + '&t=' + txid + '\x22 target=\x22ru\x22>' + txt + '</a> ';
		} 
	}
	return r;
}

function escape_html_chars(s)
{
	return s.replace(/&/g,'%AMP%').replace(/</g,'&#060;').replace(/>/g,'&#062;').replace(/"/g,'&#034;').replace(/'/g,'&#039;').replace(/%AMP%/g,'&#038;').replace(/\x0d/g,'<br />');
}

function escape_apostrophes(s)
{
	return s.replace(/'/g,'\\\'');
}

function selectToggle(toggle, form) {
	var myForm = document.forms[form];
	for( var i=0; i < myForm.length; i++ ) { 
		if (toggle) {
			myForm.elements[i].checked = "checked";
		} 
		else {
			myForm.elements[i].checked = "";
		}
	}
	markClick();
}

function multiActionGo(f,sel) {
	if ((typeof f != 'undefined') && (typeof sel != 'undefined')) {
		var v = sel.value;
		var t = sel.options[sel.selectedIndex].text;
		if (typeof v == 'string') {
			if (v == 'addtag' || v == 'deltag') {
				var notok = 1;
				var answer = '';
				while (notok) {
					answer = prompt('*** ' + t + ' ***\n\n*** ' + $('input.markcheck:checked').length + ' Record(s) will be affected ***\n\nPlease enter one tag (20 char. max., no spaces, no commas -- or leave empty to cancel:', answer); 
					if (typeof answer == 'object') answer = '';
					if (answer.indexOf(' ') > 0 || answer.indexOf(',') > 0) {
						alert ('Please no spaces or commas!');
					}
					else if (answer.length > 20) {
						alert ('Please no tags longer than 20 char.!');
					}
					else {
						notok = 0;
					}	
				}
				if (answer != '') {
					f.data.value = answer;
					f.submit();
				}
			} 
			else if (v == 'del' || v == 'smi1' || v == 'spl1' || v == 's1' || v == 's5' || v == 's98' || v == 's99' || v == 'today' || v == 'delsent' || v == 'lower' || v == 'cap') {
				var answer = confirm ('*** ' + t + ' ***\n\n*** ' + $('input.markcheck:checked').length + ' Record(s) will be affected ***\n\nAre you sure?'); 
				if (answer) { 
					f.submit();
				}
			} 
			else {
				f.submit();
			}
		} 
		sel.value='';
	}
}

function allActionGo(f,sel,n) {
	if ((typeof f != 'undefined') && (typeof sel != 'undefined')) {
		var v = sel.value;
		var t = sel.options[sel.selectedIndex].text;
		if (typeof v == 'string') {
			if (v == 'addtagall' || v == 'deltagall') {
				var notok = 1;
				var answer = '';
				while (notok) {
					answer = prompt('THIS IS AN ACTION ON ALL RECORDS\nON ALL PAGES OF THE CURRENT QUERY!\n\n*** ' + t + ' ***\n\n*** ' + n + ' Record(s) will be affected ***\n\nPlease enter one tag (20 char. max., no spaces, no commas -- or leave empty to cancel:', answer); 
					if (typeof answer == 'object') answer = '';
					if (answer.indexOf(' ') > 0 || answer.indexOf(',') > 0) {
						alert ('Please no spaces or commas!');
					}
					else if (answer.length > 20) {
						alert ('Please no tags longer than 20 char.!');
					}
					else {
						notok = 0;
					}	
				}
				if (answer != '') {
					f.data.value = answer;
					f.submit();
				}
			} 
			else if (v == 'delall' || v == 'smi1all' || v == 'spl1all' || v == 's1all' || v == 's5all' || v == 's98all' || v == 's99all' || v == 'todayall' || v == 'delsentall' || v == 'capall' || v == 'lowerall') {
				var answer = confirm ('THIS IS AN ACTION ON ALL RECORDS\nON ALL PAGES OF THE CURRENT QUERY!\n\n*** ' + t + ' ***\n\n*** ' + n + ' Record(s) will be affected ***\n\nARE YOU SURE?'); 
				if (answer) { 
					f.submit();
				}
			} else {
				f.submit();
			}
		} 
		sel.value='';
	}
}

function areCookiesEnabled() {
	setCookie( 'test', 'none', '', '/', '', '' );
	if ( getCookie( 'test' ) ) {
		cookie_set = true;
		deleteCookie('test', '/', '');
	} else {
		cookie_set = false;
	}
	return cookie_set;
}

function setLang(ctl,url) {
	location.href = 'save_setting_redirect.php?k=currentlanguage&v=' + 
	ctl.options[ctl.selectedIndex].value + 
	'&u=' + url;
}

function resetAll(url) {
	location.href = 'save_setting_redirect.php?k=currentlanguage&v=&u=' + url;
}

function getCookie(check_name) {
	var a_all_cookies = document.cookie.split( ';' );
	var a_temp_cookie = '';
	var cookie_name = '';
	var cookie_value = '';
	var b_cookie_found = false; // set boolean t/f default f
	var i = '';
	for ( i = 0; i < a_all_cookies.length; i++ ) {
		a_temp_cookie = a_all_cookies[i].split( '=' );
		cookie_name = a_temp_cookie[0].replace(/^\s+|\s+$/g, '');
		if ( cookie_name == check_name ) {
			b_cookie_found = true;
			if ( a_temp_cookie.length > 1 ) {
				cookie_value = unescape( a_temp_cookie[1].replace(/^\s+|\s+$/g, '') );
			}
			return cookie_value;
			break;
		}
		a_temp_cookie = null;
		cookie_name = '';
	}
	if ( ! b_cookie_found ) {
		return null;
	}
}

function setCookie( name, value, expires, path, domain, secure ) {
	var today = new Date();
	today.setTime( today.getTime() );
	if ( expires ) {
		expires = expires * 1000 * 60 * 60 * 24;
	}
	var expires_date = new Date( today.getTime() + (expires) );
	document.cookie = name + "=" +escape( value ) +
		( ( expires ) ? ";expires=" + expires_date.toGMTString() : "" ) + 
		( ( path ) ? ";path=" + path : "" ) + 
		( ( domain ) ? ";domain=" + domain : "" ) +
		( ( secure ) ? ";secure" : "" );
}

function deleteCookie( name, path, domain ) {
	if ( getCookie( name ) ) document.cookie = name + "=" +
		( ( path ) ? ";path=" + path : "") +
		( ( domain ) ? ";domain=" + domain : "" ) +
		";expires=Thu, 01-Jan-1970 00:00:01 GMT";
}
 
function iknowall(t) {
	var answer = confirm ('Are you sure?'); 
	if (answer) 
		top.frames['ro'].location.href='all_words_wellknown.php?text=' + t;
}

function check_table_prefix(p) {
	var r = false;
	var re = /^[_a-zA-Z0-9]*$/;
	if (p.length <= 20 && p.length > 0) {
		if (p.match(re)) r = true;
	}
	if (! r) 
		alert('Table Set Name (= Table Prefix) must\ncontain 1 to 20 characters (only 0-9, a-z, A-Z and _).\nPlease correct your input.'); 
	return r;
}
