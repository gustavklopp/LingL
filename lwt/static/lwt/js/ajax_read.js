/* ALL FUNCTIONS called by interacting with the text_read :
        the main bottom-left section in text_read.html 
 it comprises also all clicking on the links inside the tooltip on text_read trigger these AJAX function: */

/* helper func for ajax_clicked_word. also called by inline func in the termform searchbox button */
function _clicked_weblink_radiobutton(dictwebpage_searched_word=null){
	var wblnk_input =$('#wblnk_search input[name=wblnk]:checked'); 
	var wblnk = wblnk_input.val();
	if (!dictwebpage_searched_word){ // it means that func is called by ajax_clicked_word
		var dictwebpage_searched_word = $('#wblnk_search').data('dictwebpage_searched_word');
	}
	var wo_id = $('#wblnk_search').data('wo_id');
	if (wblnk_input.attr('id') == 'sent_gtr'){
		ajax_dictwebpage(wblnk,'', wo_id);
	} else {
		ajax_dictwebpage(wblnk, dictwebpage_searched_word);
	}
}

/* clicking on a single word in the text 
 --> creating the form in the right top panel 
 called by: func clickword() (defined here below)
		 if status == 0: op: 'new'
	        and called by: create_link_newword: op: 'new'
	        and called by: create_link_editword: op: 'edit' 
	@return an AJAX obj: allows to abort the previous AJAX if another call arrives */
function ajax_clicked_word(wo_id, show_compoundword, op, rtl) {

	// we return an object to be able to interrupt the function if another request comes
	var $ajaxClickedWord = $.ajax({url: '/termform/', type: 'GET',
			data: {
					'op' : op, 
					'wo_id' : wo_id, 
					'show_compoundword' : show_compoundword,
					'RTL': RTL
					},
			success: function(data){
				var data = JSON.parse(data);
				var dictwebpage_searched_word = data['dictwebpage_searched_word'];
				$('#topright.text_read').html(data['html']); // show the termform at the topright
				ajax_dictwebpage(WBLINK1, dictwebpage_searched_word); // and the dictwebpage at the bottomright
				
				var r = _display_possiblesimilarword(data, wo_id);
				$('#result_possiblesimilarword').html(r);
				
			},

			 error : function(data , status , xhr){ 
				if (data.statusText != 'abort'){ // Aborting is a normal process that I've coded for this func
					console.log(data); console.log(status); console.log(xhr);
					} 
				}
			});
	return $ajaxClickedWord;
}

/* same as ´func ajax_clicked_word but for compound word:
   Ctrl+click on a word in a text (i.e: wanting to create a compound word)
   --> creating form for the compoundword in the topright panel: */
function ajax_ctrlclicked_compoundword(wo_id, op, rtl) {
	/* called by: text_read_clickevent + Ctrl */
	$.ajax({url: '/termform/', type: 'GET',
			data: {
				'op':op, 
				'compoundword_id_list': JSON.stringify(compoundword_id_list)},
				// compoundword_id_list is directly defined inside the html (<script></script> section)
			success: function(data){
				var data = JSON.parse(data);
				$('#topright.text_read').html(data['html']); // show the termform at the topright
				var dictwebpage_searched_word = data['dictwebpage_searched_word'];
				ajax_dictwebpage(WBLINK1, dictwebpage_searched_word); // and the dictwebpage at the bottomright

				var r = _display_possiblesimilarword(data, wo_id);
				$('#result_possiblesimilarword').html(r);
				
				/* clicking on the radio button in termform to choose link */
				$('#wblnk_search input').change(function() {
					var wblnk = $('input[name=wblnk]:checked').val()
					var dictwebpage_searched_word = $('#wblnk_search').data('dictwebpage_searched_word');
					ajax_dictwebpage(wblnk, dictwebpage_searched_word);
				});
			},
			 error : function(data , status , xhr){ console.log(data); console.log(status); console.log(xhr);}
			});
}


/* BROWSE DICT WEBPAGE : sends by AJAX data to refresh the bottom right of text_read 
 with the dict webpage inside 
 @WBLINK: it´s WBLINK1 (url to dict1), or WBLINK2 (for dict2) or Google (WBLINK3) 
 @phrase: the text of the word (it´s in attribute ´wowordtext´ also
 @issentence: it´s the id of the word. put ´´ in fact if it´s not a sentence. */
function ajax_dictwebpage(WBLINK, phrase, issentence) {

		// case (OUTDATED): it's a dict API: AJAX fetches the JSON on the wwww,
		// (in fact, API on Glosbe doesn't work anymore...)
		if (WBLINK.indexOf('glosbe.com/gapi') != -1){
			$.ajax({url: WBLINK, type: 'GET',
					dataType: 'jsonp',
					data: {'phrase': phrase, 'issentence': issentence},
					success: function(data){ 
						// the JSON obj from the www is sent to the view dictwebpage which processes it and 
						$.ajax({url: '/dictwebpage', type: 'GET', 
								data: {'json_obj':JSON.stringify(data)},
								// sends back html.
								success: function(data){$('#bottomright.text_read').html(data);}
								});
					}
					});
		}
		// Case where Opening in a new window with the url given
		else if (WBLINK.charAt(0) == '*') {	
			$.ajax({url: '/dictwebpage/', type: 'GET',
					dataType: 'json',
					data: {'word': phrase, 'wbl': WBLINK, 'issentence': issentence},
					// and the view sends backs a JSON containing the string URL. <iframe> displays it then.
					success: function(data){
								var params = 'width='+window.innerWidth/2+', height='+window.innerHeight*0.7+', ';
								params += 'top='+window.innerHeight/2+', left='+window.innerWidth/2+', ';
								params += ' scrollbars=yes, menubar=no, resizable=yes, status=no';
								window.open(data,'dictwin', params);
							
							},
					 error : function(data , status , xhr){ console.log(data); console.log(status); console.log(xhr); }
					});
			}
		// Case where Not using iframe but scraping of the url. Note: 'sandbox' allows to deactivate link inside iframe
		else if (WBLINK.charAt(0) == '^'){ 
			$.ajax({url: '/dictwebpage/', type: 'GET',
					dataType: 'json',
					data: {'word': phrase, 'wbl': WBLINK, 'issentence': issentence},
					// and the view sends backs a JSON containing the string URL. <iframe> displays it then.
					success: function(data){
								$('#bottomright.text_read').html('<span class="iframe_container"><iframe class="text_read nolink_iframe" id="dictwebpage" src="about:blank" srcdoc="'+data+'"></iframe></span>');
							},
					 error : function(data , status , xhr){ console.log(data); console.log(status); console.log(xhr); }
					});
			}
		// Case where the dictionary uses an API (for ex. with Google translate)
		 else if (WBLINK.charAt(0) == '!' || WBLINK.charAt(0) == '#'){
			$.ajax({url: '/dictwebpage/', type: 'GET',
					data: {'word': phrase, 'wbl': WBLINK, 'issentence': issentence},
					// and the view sends backs a JSON containing the string URL. <iframe> displays it then.
					success: function(data){
								$('#bottomright.text_read').html(data);
							},
					 error : function(data , status , xhr){ console.log(data); console.log(status); console.log(xhr); }
					});
			}
		// Case where opening the webpage dict in an iframe with the url given
		else {	
			$.ajax({url: '/dictwebpage/', type: 'GET',
					dataType: 'json',
					data: {'word': phrase, 'wbl': WBLINK, 'issentence': issentence},
					// and the view sends backs a JSON containing the string URL. <iframe> displays it then.
					success: function(data){
								$('#bottomright.text_read').html('<iframe class="text_read" id="dictwebpage" src="'+data+'"></iframe>');
								// check that crossdomain is authorized in iframe:
								// NOT WORKING
								//var iframe = document.getElementsByTagName('iframe')[0];
								//var doc = iframe.contentDocument || iframe.contentWindow.document;
								//var booltest = Boolean(document.getElementsByTagName('iframe')[0].contentDocument);
								/*
								var m = '<p>'+gettext("This dictionary website forbids fetching its data from third parties.")+'</p>';
								m += '<p>'+gettext("You should edit your language and change the URL.")+'</p>';
								m += '<p>'+gettext("For example you could try to insert a '^' before the URL to make LingLibre try scraping the website.")+'</p>';
								m += '<p>'+gettext("(see the Help page for more info.)")+'</p>';
								$('#bottomright.text_read').html('<iframe class="text_read" id="dictwebpage" src="about:blank" srcdoc="'+m+'"></iframe>');
								*/
							},
					 error : function(data , status , xhr){ console.log(data); console.log(status); console.log(xhr); }
					});
			}
}

/* mark all the remaining words in the sentence as known */
function iknowall(event, wo_id){
	//the current selected word:
	var sel_word = DOCUMENT.find('.clicked');;
	var wo_id = sel_word.attr('woid');
	$.ajax({url: '/iknowall/', 
			type: 'GET',
			dataType: 'json',
			data: 
				{ 
					'wo_id':wo_id,
				},
			success: function(data){ 
				$('#topright.text_read').html(data['html']); 
				// update status of the word and the counter at the top
				$.each(data['wo_id_to_update_in_ajax'], function(idx, val){ // val=wo_id
						update_status(val, '', data['wostatus']);
						//update the title in word also
						update_title(val, data['iscompoundword'], data['wowordtext'], 
						  data['wotranslation'], data['woromanization'], data['wostatus'],
						  data['cowordtext'],data['cowotranslation'], data['coworomanization'], data['cowostatus'],
						  data['show_compoundword']);
					});
				// and move to the next sentence if it's not the last known
				if(data['firstWord_of_nextSentence']){
					var sel_word = DOCUMENT.find('.clicked'); //don't know why but I need to re-get this...
					sel_word.removeClass('clicked');
					var sel_word = DOCUMENT.find('span[woid="'+data['firstWord_of_nextSentence']+'"]');
					sel_word.addClass('clicked');	
					click_ctrlclick_toggle(sel_word, event); // creating: clicktooltip and the right panel (bottom & top)
					// and autoscroll to it
					_autoscroll_to_sel_word(sel_word);
				}
			},
			error : function(data , status , xhr){ console.log(data); console.log(status); console.log(xhr);
			}
	});	
}