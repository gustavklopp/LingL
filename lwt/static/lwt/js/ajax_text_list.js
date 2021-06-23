/* dynamic filtering when check/unckeck the ckeckbox */
function textlist_filter() {
	// get the form
	var filterlangform = $('#filterlangform');
	var filtertagform = $('#filtertagform');
	var timeform = $('#timeform');
	var filterarchivedform = $('#archivedform');

	// get what are the checkbox checked for: language
	// and also get the texts Ids for the chosen langs:
	var chosen_lang = [];
	var chosenlang_textIds = []
	var checkedlang_nb = 0
	$.each($("#filterlangform input:checked"), function(){
		checkedlang_nb += 1;
		chosen_lang.push(parseInt($(this).val()));
		var textIds = $(this).data('textids');
		chosenlang_textIds = chosenlang_textIds.concat(textIds);
		
	});
	// show column or hide column language if there's more than one language
	if (checkedlang_nb == 1){
		$('#text_table').bootstrapTable('hideColumn', 'language');	
	} else {
		$('#text_table').bootstrapTable('showColumn', 'language');	
	}
	/*
	//if nothing was chosen, display a warning
	if (chosen_lang.length === 0){
		$('#no_langfilter').text(gettext('No language chosen: no texts will be displayed'));
	} else {
		$('#no_langfilter').text('');
	} */

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

	// get what are the checkbox checked for: Archived
	var chosen_archived = [];
	$.each(filterarchivedform.find("span").find("input"), function(){
		if ($(this).is(':checked')){
			chosen_archived.push($(this).val());
		}
		var archived_textIds = $(this).data('textids');
		if (isdisjoint(chosenlang_textIds, archived_textIds)){
			$(this).next().attr('class', 'checkboxitem-normal');
		} else {
			$(this).next().attr('class', 'checkboxitem-bold');
		}
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
			
		},
		error : function(data , status , xhr){ console.log('ERROR');//error console.log(data); console.log(status); console.log(xhr);
		}
	});
}

