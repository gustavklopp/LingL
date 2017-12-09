function isdisjoint(array1, array2){
	/* helper function for textlist_filter: equivalent to python .isdisjoint */
	var toReturn = true;
	$.each(array1, function(idx, el){
		if ($.inArray(el, array2) !== -1) { 
			toReturn = false; // because the return false only stop the loop but doesn't return the function! 
			return false;
			}
	});
	return toReturn;
}

function textlist_filter() {
	/* dynamic filtering when check/unckeck the ckeckbox */
	// get the form
	var filterlangform = $('#filterlangform');
	var filtertagform = $('#filtertagform');
	var timeform = $('#timeform');
	var archivedform = $('#archivedform');
	var chosen_lang = [];
	// get the checkbox checked
	$.each($("#filterlangform input:checked"), function(){
		chosen_lang.push(parseInt($(this).val()));
	});
	var chosen_tag = [];
	$.each($("#filtertagform").find("span").not(".hidden").find("input:checked"), function(){
		chosen_tag.push($(this).val());
	});
	var chosen_time = [];
	$.each($("#timeform").find("span").not(".hidden").find("input:checked"), function(){
		chosen_time.push($(this).val());
	});
	var chosen_archived = [];
	$.each($("#archivedform").find("span").not(".hidden").find("input:checked"), function(){
		chosen_archived.push($(this).val());
	});
	// stringify them
	var chosen_lang_json = JSON.stringify(chosen_lang);
	var chosen_tag_json = JSON.stringify(chosen_tag);
	var chosen_time_json = JSON.stringify(chosen_time);
	var chosen_archived_json = JSON.stringify(chosen_archived);
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
	data_to_go.append('archived_filter', chosen_archived_json);
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

