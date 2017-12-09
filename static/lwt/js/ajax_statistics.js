/*
function openPage(ev){
	var statusnumber = $('#chart-statusnumber');
	console.log(statusnumber);
	var activePoints = statusnumber.getElementsAtEvent(ev);
	var firstPoint = activePoints[0];
	var label = statusnumber.data.labels[firstPoint._index];
	var value = statusnumber.data.datasets[firstPoint._datasetIndex].data[firstPoint._index];
	if (firstPoint !== undefined)
		alert(label + ": " + value);
}
*/
function ajax_filterlangform_submit(lang_id, currentlang_id){
	$.get('/statistics/line_chart/'+lang_id+'/', function(configuration) {
	/* drawing the bar char */
		/* make the language filter in bold */
			if (lang_id != currentlang_id){ // leave the <strong> if it's initialization
				// remove the <strong> for all:
				$('#ul_language li a strong').each(function(index, value){
					$(this).contents().unwrap();
				});
				// put the <strong>:
				$('#ul_language li a#'+lang_id).contents().wrap('<strong></strong>');
			}
			
		/* display the bar chart */
		var data = configuration['data'];
		if (typeof LineNewChart != 'undefined'){
			LineNewChart.destroy();
		}
		var ctx = document.getElementById("chart-wordnumber").getContext("2d");    

		if (lang_id == 'total'){ /* display the stacked bar chart */
			LineNewChart = new Chart(ctx, { 
									data : data,
									type : 'bar',
									options: {
									        scales : {
									            'yAxes':  [{
									            	ticks: { 'min': 0 },
									            	stacked: true,
													scaleLabel: {
														display: true,
														labelString: gettext('Nb of words created / week')
													}
									            }],
												'xAxes':  [{
													stacked: true
												}]
									            }
									}
			}) ;
		} else {
			LineNewChart = new Chart(ctx, { 
									data : data,
									type : 'bar',
									options: {
									        scales : {
									            'yAxes':  [{
									            	ticks: { 'min': 0 },
													scaleLabel: {
														display: true,
														labelString: gettext('Nb of words created / week')
													}
									            }]
									            }
									}
			}) ;
		}

	});
	$.get('/statistics/pie_chart/'+lang_id+'/', function(configuration) {
	/* drawing the pie chart */
		var data = configuration['data'];
		if (typeof PieNewChart != 'undefined'){
			PieNewChart.destroy();
		}
		var ctx = document.getElementById("chart-statusnumber").getContext("2d");    

		PieNewChart = new Chart(ctx, { 
								data : data,
								type : 'pie',
								options: { 
									onClick: function(ev){ openPage(ev)}
									}
			});
	});
}
