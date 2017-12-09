function convert_true_to_True(val){
	/* because json gives back a bool whereas to set the select html we need a string */
	if (val == true){
		return 'True';
	} else if (val == false){
		return 'False';
	}
}

function ajax_fill_language_detail(code_lang){
	/* from the language code, get the data for the given language */
	
	$.ajax({url: '/fill_language_detail/', type: 'GET',
			type: 'GET',
			dataType: 'json',
			data: {
					'code_lang' : code_lang, 
					},
			success: function(data){
				$('ul#list__dict1uri').empty() // remove all the children
				$('ul#list__dict2uri').empty()
				$('ul#list__dict1uri ').next().addClass('hidden'); // and make hidden 
				$('ul#list__dict2uri ').next().addClass('hidden'); 
				$.each(data['dicturi'], function(index, value){
					$('ul#list__dict1uri').append('<li><a href="#" data-value="'+value+'">'+value+'</a></li>'); 
					if (index == 0){
						$('input#id_dict1uri').val(value); 
					}
					$('ul#list__dict1uri ').next().removeClass('hidden'); 
				});
				$.each(data['dicturi'], function(index, value){
					$('ul#list__dict2uri').append('<li><a href="#" data-value="'+value+'">'+value+'</a></li>'); 
					if (index == 0){
						$('input#id_dict2uri').val(value); 
					$('ul#list__dict2uri ').next().removeClass('hidden'); 
					}
				});
				// bind them to a click 
			  $("#list__dict1uri.dropdown-menu a").bind('click', function(event) {
				$("input#id_dict1uri").val($(this).text());
			  });
			  $("#list__dict2uri.dropdown-menu a").bind('click', function(event) {
				$("input#id_dict2uri").val($(this).text());
			  });
				$('input#id_googletranslateuri').val(data['googletranslateuri']); 
				$('input#id_exporttemplate').val(data['exporttemplate']); 
				$('select#id_textsize').val(data['textsize'].toString());  // don't forget to convert the int to string
				$('input#id_charactersubstitutions').val(data['charactersubstitutions']); 
				$('input#id_regexpsplitsentences').val(data['regexpsplitsentences']); 
				$('input#id_exceptionssplitsentences').val(data['exceptionssplitsentences']); 
				$('input#id_regexpwordcharacters').val(data['regexpwordcharacters']); 
				$('select#id_removespaces').val(convert_true_to_True(data['removespaces'])); 
				$('select#id_spliteachchar').val(convert_true_to_True(data['spliteachchar'])); 
				$('select#id_righttoleft').val(convert_true_to_True(data['righttoleft'])); 
				$('input#id_code_639_1').val(data['code_639_1']); 
				$('input#id_code_639_2b').val(data['code_639_2b']); 
				$('input#id_code_639_2t').val(data['code_639_2t']); 
				$('input#id_django_code').val(data['django_code']); 
			},
			 error : function(data , status , xhr){ console.log(data); console.log(status); console.log(xhr);}
			});
	
}