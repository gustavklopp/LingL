/* ALL FUNCTIONS called by interacting with the text_read :
        the main bottom-left section in text_read.html 
 it comprises also all clicking on the links inside the tooltip on text_read trigger these AJAX function: */

function ajax_clicked_word(wo_id, show_compoundword, op, rtl) {
	/* called by: text_read_clickevent, if status == 0: op: 'new'
	        and: create_link_newword: op: 'new'
	        and: create_link_editword: op: 'edit' */
	$.ajax({url: '/termform/', type: 'GET',
			data: {
					'op' : op, 
					'wo_id' : wo_id, 
					'show_compoundword' : show_compoundword,
					'RTL': RTL
					},
			success: function(data){
				var data = JSON.parse(data);
				$('#topright.text_read').html(data['html']); // show the termform at the topright
				var dictwebpage_searched_word = data['dictwebpage_searched_word'];
				ajax_dictwebpage(WBLINK1, dictwebpage_searched_word); // and the dictwebpage at the bottomright
			},
			 error : function(data , status , xhr){ console.log(data); console.log(status); console.log(xhr);}
			});
}

/* creating form for the compoundword: */
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
			},
			 error : function(data , status , xhr){ console.log(data); console.log(status); console.log(xhr);}
			});
}

// CREATING A NEW WORD:  sends by AJAX data to refresh the top right of text_read with the form termform// or EDITING A WORD:

function ajax_termform(wo_id, op, rtl) {
	/* called by: text_read_clickevent, if status == 0: op: 'new'
	        and: create_link_newword: op: 'new'
	        and: create_link_editword: op: 'edit' */
	$.ajax({url: '/termform/', type: 'GET',
			data: {'op':op, 'wo_id': wo_id},
			success: function(data){
				$('#topright.text_read').html(data);
			},
			 error : function(data , status , xhr){
					console.log(data);
					console.log(status);
					console.log(xhr);}
			});
}


function ajax_del_word(wo_id) {
	/* delete a word and the similar words and compoundword with it */
	$.ajax({url: '/termform/', 
			type: 'GET',
			dataType: 'json',
			data: 
				{ 
					'op':'del', 'wo_id' : wo_id,
				},
			success: function(data){ 
				$('#topright.text_read').html(data['html']); 
				ajax_update_word_simword_compoundword(data, 'del');
			},
			error : function(data , status , xhr){ console.log('ERROR');//error console.log(data); console.log(status); console.log(xhr);
			}
	});
}

function ajax_del_singleword(wo_id) {
	/* same as above but we delete only one single word, not the similar words with it */
	$.ajax({url: '/termform/', 
			type: 'GET',
			dataType: 'json',
			data: 
				{ 
					'op':'del', 'wo_id' : wo_id, 'singleword': true,
				},
			success: function(data){ 
				$('#topright.text_read').html(data['html']); 
				// update status of the word and the counter at the top
				update_status(wo_id, 'del');
				$('span[woid='+wo_id+']').attr('title', create_tooltip_title('▶',data['wowordtext'],'','','0'));
			},
			error : function(data , status , xhr){ console.log('ERROR');//error console.log(data); console.log(status); console.log(xhr);
			}
	});
}


/* BROWSE DICT WEBPAGE : sends by AJAX data to refresh the bottom right of text_read 
 with the dict webpage inside */
function ajax_dictwebpage(WBLINK, phrase, issentence) {

		// case 1: it's a dict API: AJAX fetches the JSON on the wwww,
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
		else {	// case 2: it's a simple dict webpage: AJAX sends the link to process to the view dictwebpage,
			$.ajax({url: '/dictwebpage/', type: 'GET',
					dataType: 'json',
					data: {'word': phrase, 'wbl': WBLINK, 'issentence': issentence},
					// and the view sends backs a JSON containing the string URL. <iframe> displays it then.
					success: function(data){
							if (data.charAt(0) == '*'){ // frame embedding blocked, open new tab
								window.open(data.slice(1),'dictwin', 
										'width=800, height=400, scrollbars=yes, menubar=no, resizable=yes, status=no');
								} else { // open the webpage dict in an iframe
								$('#bottomright.text_read').html('<iframe class="text_read" id="dictwebpage" src="'+data+'"></iframe>');
								}
							},
					 error : function(data , status , xhr){ console.log(data); console.log(status); console.log(xhr); }
					});
			}

}


