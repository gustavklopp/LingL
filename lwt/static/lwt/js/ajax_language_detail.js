/* because json gives back a bool whereas to set the select html we need a string */
function convert_true_to_True(val){
	if (val == true){
		return 'True';
	} else if (val == false){
		return 'False';
	}
}

/* on Text Detail Form: clicking on the select arrow button on the right: 
	it displays a list of Predefined Language.
   Choosing one of them (i.e: get their language code), it automatically fills in all the field
   in the Language Edit form for the given language */
function ajax_fill_language_detail(code_lang){
	$.ajax({url: '/fill_language_detail/', type: 'GET',
			type: 'GET',
			dataType: 'json',
			data: {
					'code_lang' : code_lang, 
					},
			success: function(data){
				$('div#list__dict1uri').empty() // remove all the children
				$('div#list__dict2uri').empty()
				$('div#list__dict1uri ').next().addClass('hidden'); // and make hidden 
				$('div#list__dict2uri ').next().addClass('hidden'); 
				var dicturi_list = data['dicturi'].split(',');
				$.each(dicturi_list, function(index, value){
					if (index == 0){ //default inside the input
						$('input#id_dict1uri').val(value.trim()); 
					}
					if (index == 1){ //default inside the input
						$('input#id_dict2uri').val(value.trim()); 
					}
					$('div#list__dict1uri').append('<a class="dropdown-item" href="#" data-value="'+value+'">'+value+'</a>'); 
					$('div#list__dict2uri').append('<a class="dropdown-item"  href="#" data-value="'+value+'">'+value+'</a>'); 
				});
				if (dicturi_list.length > 1){ // show the button if there's enough dicturi to show
					$('#input-group-append_list__dict1uri ').removeClass('hidden'); 
					$('#input-group-append_list__dict2uri ').removeClass('hidden'); 
				}
				// put also dicturi inside the hidden field dicturi 
				$('input#id_dicturi').val(data['dicturi']);

				// bind them to a click 
			  $("#list__dict1uri.dropdown-menu a").bind('click', function(event) {
				$("input#id_dict1uri").val($(this).text());
			  });
			  $("#list__dict2uri.dropdown-menu a").bind('click', function(event) {
				$("input#id_dict2uri").val($(this).text());
			  });
				//$('input#id_dict1uri').val(data['dict1uri']); 
				//$('input#id_dict2uri').val(data['dict2uri']); 
				$('input#id_googletranslateuri').val(data['googletranslateuri']); 
				$('textarea#id_exporttemplate').val(data['exporttemplate']); 
				$('select#id_textsize').val(data['textsize'].toString());  // don't forget to convert the int to string
				$('input#id_charactersubstitutions').val(data['charactersubstitutions']); 
				$('input#id_regexpsplitsentences').val(data['regexpsplitsentences']); 
				$('input#id_exceptionssplitsentences').val(data['exceptionssplitsentences']); 
				$('input#id_regexpwordcharacters').val(data['regexpwordcharacters']); 
				$('select#id_removespaces').val(convert_true_to_True(data['removespaces'])); 
				$('select#id_spliteachchar').val(convert_true_to_True(data['spliteachchar'])); 
				$('select#id_has_romanization').val(convert_true_to_True(data['has_romanization'])); 
				$('select#id_righttoleft').val(convert_true_to_True(data['righttoleft'])); 
				$('input#id_code_639_1').val(data['code_639_1']); 
				$('input#id_code_639_2b').val(data['code_639_2b']); 
				$('input#id_code_639_2t').val(data['code_639_2t']); 
				$('input#id_django_code').val(data['django_code']); 
			},
			 error : function(data , status , xhr){ console.log(data); console.log(status); console.log(xhr);}
			});
	
}