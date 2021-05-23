/* helper function for textlist_filter: equivalent to python set.isdisjoint 
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

/* dynamic filtering when check/unckeck the ckeckbox */
function textlist_filter() {
	// get the form
	var filterlangform = $('#filterlangform');
	var filtertagform = $('#filtertagform');
	var timeform = $('#timeform');

	// get what are the checkbox checked for: language
	// and also get the texts Ids for the chosen langs:
	var chosen_lang = [];
	var chosenlang_textIds = []
	$.each($("#filterlangform input:checked"), function(){
		chosen_lang.push(parseInt($(this).val()));
		var textIds = $(this).data('textids');
		chosenlang_textIds = chosenlang_textIds.concat(textIds);
	});
	//if nothing was chosen, display a warning
	if (chosen_lang.length === 0){
		$('#no_langfilter').text(gettext('No language chosen: no texts will be displayed'));
	} else {
		$('#no_langfilter').text('');
	}

	// get what are the checkbox checked for: tags
	var chosen_tag = [];
	$.each(filtertagform.find("span").find("input"), function(){
		if ($(this).is(':checked')){
			chosen_tag.push($(this).val());
		}
		var tag_textIds = $(this).data('textids');
		if (isdisjoint(chosenlang_textIds, tag_textIds)){
			$(this).next().attr('class', 'checkboxitem-normal');
		} else {
			$(this).next().attr('class', 'checkboxitem-bold');
		}
	});

	// get what are the checkbox checked for: time
	var chosen_time = [];
	$.each(timeform.find("span").find("input"), function(){
		if ($(this).is(':checked')){
			chosen_time.push($(this).val());
		}
		var time_textIds = $(this).data('textids');
		if (isdisjoint(chosenlang_textIds, time_textIds)){
			$(this).next().attr('class', 'checkboxitem-normal');
		} else {
			$(this).next().attr('class', 'checkboxitem-bold');
		}
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
			
		},
		error : function(data , status , xhr){ console.log('ERROR');//error console.log(data); console.log(status); console.log(xhr);
		}
});
}

