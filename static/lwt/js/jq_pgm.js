/**************************************************************
Global variables used in LWT jQuery functions
***************************************************************/

var TEXTPOS = -1;
var OPENED = 0;
var WID = 0;
var TID = 0;
var WBLINK1 = '';
var WBLINK2 = '';
var WBLINK3 = '';
var SOLUTION = '';
var ADDFILTER = '';
var RTL = 0;
var ANN_ARRAY = {};
 
/**************************************************************
LWT jQuery functions
***************************************************************/

function setTransRoman(tra, rom) {
	if($('textarea[name="WoTranslation"]').length == 1)
		$('textarea[name="WoTranslation"]').val(tra);
	if($('input[name="WoRomanization"]').length == 1)
		$('input[name="WoRomanization"]').val(rom);
	makeDirty();
}

function getUTF8Length(string) {
	var utf8length = 0;
	for (var n = 0; n < string.length; n++) {
		var c = string.charCodeAt(n);
		if (c < 128) {
			utf8length++;
		}
		else if((c > 127) && (c < 2048)) {
			utf8length = utf8length+2;
		}
		else {
			utf8length = utf8length+3;
		}
	}
	return utf8length;
}

function scrollToAnchor(aid){
  document.location.href = '#' + aid;
}

function changeImprAnnText() {
	var textid = $('#editimprtextdata').attr('data_id');
	$(this).prev('input:radio').attr('checked', 'checked');
	var elem = $(this).attr('name');
	var thedata = JSON.stringify($('form').serializeObject());
	$.post('ajax_save_impr_text.php', { id: textid, elem: elem, data : thedata }
		, function(d) { 
				if(d != 'OK') 
					alert('Saving your changes failed, please reload page and try again!'); 
			} 
	);
}
 
function changeImprAnnRadio() {
	var textid = $('#editimprtextdata').attr('data_id');
	var elem = $(this).attr('name');
	var thedata = JSON.stringify($('form').serializeObject());
	$.post('ajax_save_impr_text.php', { id: textid, elem: elem, data : thedata }
		, function(d) { 
				if(d != 'OK') 
					alert('Saving your changes failed, please reload page and try again!'); 
			} 
	);
}

function addTermTranslation(wordid,txid,word,lang) {
	var thedata = $(txid).val().trim();
	var pagepos = $(document).scrollTop();
	if((thedata == '') || (thedata == '*')) {
		alert('Text Field is empty or = \'*\'!');
		return;
	}
	$.post('ajax_add_term_transl.php', { id: wordid, data : thedata, text: word, lang: lang }
		, function(d) { 
				if(d == '') {
					alert('Adding translation to term OR term creation failed, please reload page and try again!'); 
				} else {
					do_ajax_edit_impr_text(pagepos,d);
				}
			} 
	);
}

function isInt(value) {
	for (i = 0 ; i < value.length ; i++) {
		if ((value.charAt(i) < '0') || (value.charAt(i) > '9')) {
			return false;
		}
	}
	return true;
}


function textareaKeydown(event) {
	if (event.keyCode && event.keyCode == '13') {
		if (check()) $('input:submit').last().click();
		return false;
	} else {
		return true;
	}
}


// Keyboard shortcuts for test portion:
// TODO: test not yet implemented
// Keyboard shortcuts. in Text_read. 
/* NOT USED IN FACT
function text_read_keydownevent(e) {

	if (e.which == 27) {  // esc = reset all
		TEXTPOS = -1;
		$('span.uwordmarked').removeClass('uwordmarked');
		$('span.kwordmarked').removeClass('kwordmarked');
		cClick();
		return false;
	}
	
	if (e.which == 13) {  // return = edit next unknown word
		$('span.uwordmarked').removeClass('uwordmarked');
		var unknownwordlist = $('span.status0.word:not(.hide):first');
		if (unknownwordlist.size() == 0) return false;
		$(window).scrollTo(unknownwordlist,{axis:'y', offset:-150});
		unknownwordlist.addClass('uwordmarked').click();
		cClick();
		return false;
	}
	
	var knownwordlist = $('span.word:not(.hide):not(.status0)' + ADDFILTER + ',span.mword:not(.hide)' + ADDFILTER);
	var l_knownwordlist = knownwordlist.size();
	if (l_knownwordlist == 0) return true;
	
	// the following only for a non-zero known words list
	if (e.which == 36) {  // home : known word navigation -> first
		$('span.kwordmarked').removeClass('kwordmarked');
		TEXTPOS = 0;
		curr = knownwordlist.eq(TEXTPOS);
		curr.addClass('kwordmarked');
		$(window).scrollTo(curr,{axis:'y', offset:-150});
		var ann = '';
		if ((typeof curr.attr('data_ann')) != 'undefined') 
			ann = curr.attr('data_ann');
		window.parent.frames['ro'].location.href = 'show_word.php?wid=' + curr.attr('data_wid') + '&ann=' + encodeURIComponent(ann);
		return false;
	}
	if (e.which == 35) {  // end : known word navigation -> last
		$('span.kwordmarked').removeClass('kwordmarked');
		TEXTPOS = l_knownwordlist-1;
		curr = knownwordlist.eq(TEXTPOS);
		curr.addClass('kwordmarked');
		$(window).scrollTo(curr,{axis:'y', offset:-150});
		var ann = '';
		if ((typeof curr.attr('data_ann')) != 'undefined') 
			ann = curr.attr('data_ann');
		window.parent.frames['ro'].location.href = 'show_word.php?wid=' + curr.attr('data_wid') + '&ann=' + encodeURIComponent(ann);
		return false;
	}
	if (e.which == 37) {  // left : known word navigation
		$('span.kwordmarked').removeClass('kwordmarked');
		TEXTPOS--;
		if (TEXTPOS < 0) TEXTPOS = l_knownwordlist - 1;
		curr = knownwordlist.eq(TEXTPOS);
		curr.addClass('kwordmarked');
		$(window).scrollTo(curr,{axis:'y', offset:-150});
		var ann = '';
		if ((typeof curr.attr('data_ann')) != 'undefined') 
			ann = curr.attr('data_ann');
		window.parent.frames['ro'].location.href = 'show_word.php?wid=' + curr.attr('data_wid') + '&ann=' + encodeURIComponent(ann);
		return false;
	}
	if (e.which == 39 || e.which == 32) {  // space /right : known word navigation
		$('span.kwordmarked').removeClass('kwordmarked');
		TEXTPOS++;
		if (TEXTPOS >= l_knownwordlist) TEXTPOS = 0;
		curr = knownwordlist.eq(TEXTPOS);
		curr.addClass('kwordmarked');
		$(window).scrollTo(curr,{axis:'y', offset:-150});
		var ann = '';
		if ((typeof curr.attr('data_ann')) != 'undefined') 
			ann = curr.attr('data_ann');
		window.parent.frames['ro'].location.href = 'show_word.php?wid=' + curr.attr('data_wid') + '&ann=' + encodeURIComponent(ann);
		return false;
	}

	if (TEXTPOS < 0 || TEXTPOS >= l_knownwordlist) return true;
	var curr = knownwordlist.eq(TEXTPOS);
	var wid = curr.attr('data_wid');
	var ord = curr.attr('data_order');
	
	// the following only with valid pos.
	for (var i=1; i<=5; i++) {
		if (e.which == (48+i) || e.which == (96+i)) {  // 1,.. : status=i
			window.parent.frames['ro'].location.href = 
				'set_word_status.php?wid=' + wid + '&tid=' + TID + '&ord=' + ord + '&status=' + i;
			return false;
		}
	}
	if (e.which == 73) {  // I : status=98
		window.parent.frames['ro'].location.href = 
			'set_word_status.php?wid=' + wid + '&tid=' + TID + '&ord=' + ord + '&status=98';
		return false;
	}
	if (e.which == 87) {  // W : status=99
		window.parent.frames['ro'].location.href = 
			'set_word_status.php?wid=' + wid + '&tid=' + TID + '&ord=' + ord + '&status=99';
		return false;
	}
	if (e.which == 65) {  // A : set audio pos.
		var p = curr.attr('data_pos');
		var t = parseInt($("#totalcharcount").text(),10);	
		if ( t == 0 ) return true;
		p = 100 * (p-5) / t;
		if (p < 0) p = 0;
		if (typeof (window.parent.frames['h'].new_pos) == 'function')
			window.parent.frames['h'].new_pos(p);
		else 
			return true;
		return false;
	}
	if (e.which == 69) { //  E : EDIT
		if(curr.has('.mword'))
			window.parent.frames['ro'].location.href = 
				'edit_mword.php?wid=' + wid + '&tid=' + TID + '&ord=' + ord;
		else {
			window.parent.frames['ro'].location.href = 
				'edit_word.php?wid=' + wid + '&tid=' + TID + '&ord=' + ord;
		}
		return false;
	}

	return true;
}
*/
function do_ajax_save_setting(k, v) {
	$.post('ajax_save_setting.php', { k: k, v: v } );
}

function do_ajax_update_media_select() {
	$('#mediaselect').html('&nbsp; <img src="icn/waiting2.gif" />');
	$.post('ajax_update_media_select.php', 
		function(data) { $('#mediaselect').html(data); } 
	);
}


function do_ajax_show_similar_terms() {
	$('#simwords').html('<img src="icn/waiting2.gif" />');
	$.post('ajax_show_similar_terms.php', { lang: $('#langfield').val(), word: $('#wordfield').val() }, 
		function(data) { $('#simwords').html(data); } 
	);
}

function do_ajax_word_counts() {
	$("span[id^='saved-']").each(
		function(i) {
			var textid = $(this).attr('data_id');
			$(this).html('<img src="icn/waiting2.gif" />');
			$.post('ajax_word_counts.php', { id: textid },
				function(data) { 
					var res = eval('(' + data + ')');
					$('#total-'+textid).html(res[0]);
					$('#saved-'+textid).html(res[1]);
					$('#todo-'+textid).html(res[2]);
					$('#todop-'+textid).html(res[3]);
				}
			);
		}
	);
}

function do_ajax_edit_impr_text(pagepos, word) {
	if (word=='') $('#editimprtextdata').html('<img src="icn/waiting2.gif" />');
	var textid = $('#editimprtextdata').attr('data_id');
	$.post('ajax_edit_impr_text.php', { id: textid, word: word }, 
		function(data) {
			// alert(data);
			eval(data);
			$.scrollTo(pagepos); 
			$('input.impr-ann-text').change(changeImprAnnText);
			$('input.impr-ann-radio').change(changeImprAnnRadio);
		} 
	);
}

$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};


// in replacement of PHP htmlspecialchars which translates stuff like <htmltag/> into &lt;htmltag/&gt;
function escapeHtml(str)
{
    var map =
    {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return str.replace(/[&<>"']/g, function(m) {return map[m];});
}