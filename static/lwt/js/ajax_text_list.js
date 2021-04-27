/* helper function for textlist_filter: equivalent to python .isdisjoint */
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

/* dynamic filtering when check/unckeck the ckeckbox */
function textlist_filter() {
	// get the form
	var filterlangform = $('#filterlangform');
	var filtertagform = $('#filtertagform');
	var timeform = $('#timeform');

	// get what are the checkbox checked for: language
	var chosen_lang = [];
	$.each($("#filterlangform input:checked"), function(){
		chosen_lang.push(parseInt($(this).val()));
	});
	//if nothing was chosen, display a warning
	if (chosen_lang.length === 0){
		$('#no_langfilter').text(gettext('No language chosen: no texts will be displayed'));
	} else {
		$('#no_langfilter').text('');
	}

	// get what are the checkbox checked for: tags
	var chosen_tag = [];
	$.each($("#filtertagform").find("span").not(".hidden").find("input:checked"), function(){
		chosen_tag.push($(this).val());
	});

	// get what are the checkbox checked for: time
	var chosen_time = [];
	$.each($("#timeform").find("span").not(".hidden").find("input:checked"), function(){
		chosen_time.push($(this).val());
	});
	//if nothing was chosen, display a warning
	if (chosen_time.length === 0){
		$('#no_timefilter').text(gettext('No time chosen: no texts will be displayed'));
	} else {
		$('#no_timefilter').text('');
	}

	// stringify them
	var chosen_lang_json = JSON.stringify(chosen_lang);
	var chosen_tag_json = JSON.stringify(chosen_tag);
	var chosen_time_json = JSON.stringify(chosen_time);
	// get the options for the rows per page
	var text_table = $('#text_table');
	var options = text_table.bootstrapTable('getOptions'); // get the number of rows per page
	// get the csrf token
	var token =  filterlangform.find('input[name=csrfmiddlewaretoken]').val(); // Indispensable. Get the csrf already defined in the form
	// append the data
	var data_to_go = new FormData(); // indispensable to send by POST
	data_to_go.append('lang_filter', chosen_lang_json);
	data_to_go.append('tag_filter', chosen_tag_json);
	data_to_go.append('time_filter', chosen_time_json);
	data_to_go.append('limit', options['pageSize']);
	data_to_go.append('csrfmiddlewaretoken', token);
	// and send it!
	$.ajax({url: '/textlist_filter/', 
	    type: 'POST',
		cache: false,
		processData: false,
		contentType: false,
		data:  data_to_go,
		success: function(data){ 
			text_table.bootstrapTable('load', data); 
			text_table.bootstrapTable('selectPage', 1); // go to first page
			$.each(filtertagform.find('span[language]'), function(){
				var texttag_lang = JSON.parse($(this).attr('language'));
				if (isdisjoint(texttag_lang, chosen_lang)){
					$(this).attr('class', 'hidden'); // hide the text which are not in the languages selected
				} else {
					$(this).attr('class', '');
				}
			});
		},
		error : function(data , status , xhr){ console.log('ERROR');//error console.log(data); console.log(status); console.log(xhr);
		}
});
}

