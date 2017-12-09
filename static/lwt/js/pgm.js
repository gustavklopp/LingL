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

// used inside text_list to toggle the button "Mark all" and "unMark all"
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
