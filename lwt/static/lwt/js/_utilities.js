/**************************************************************
Global variables used in LWT jQuery functions
***************************************************************/
// ?? WHICH ONES ARE USED ????
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
/* helper function for textlist_filter and termlist_filter: equivalent to python set.isdisjoint 
   check whether 2 arrays have elements in common. Return True if nothing in common */
function isdisjoint(array1, array2){
	var toReturn = true;
	$.each(array1, function(idx, el){
		if ($.inArray(el, array2) !== -1) { 
			toReturn = false; // because the return false only stop the loop but doesn't return the function! 
			return false;
			}
	});
	return toReturn;
}

/* display a loading popup when for ex. clicking on saving a text */
function display_loading_popup(popup_to_show){
	// all the background is disabled:
	$('<div></div>').appendTo('body').css({
		  'position': 'fixed',
		  'padding': '0',
		  'margin': '0',
		  'top': '0',
		  'left': '0',
		  'width': '100%',
		  'height': '100%',
		  'opacity': '0.5',
		  'background-color': 'black',
		  'z-index': '100',
	});
	// display the popup
	// the text inside the pop is found directly in the html inside the popup_to_show div
	popup_to_show.prop('hidden', false)
	.dialog({
        create: function() { 
			$(this).closest(".ui-dialog").find(".ui-dialog-titlebar:first").remove(); 
			// line below doesn't work. I've used styles.css finally
//			$(this).closest(".ui-dialog").find(".ui-dialog-content").css('min-height', '0 !important'); 
		},
		modal: true,
		zIndex: '101 !important', autoOpen: true,
		width: 'auto', resizable: false,
	   // position: {my: "center",  at: "center", of: $("body"),within: $("body") }
	}).css('background-color', 'white'); // end of '.dialog'

}

/// NOT USED FUNCTIONS ////
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