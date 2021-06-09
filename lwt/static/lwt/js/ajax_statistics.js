function create_line_chart(ctx, data){
var new_line_chart = new Chart(ctx, {
	type: 'line',
	data: data.cargo,
	options: {
		tooltips: {  /* Bug?? not showing */
			 mode: 'point',
			 enabled: true,
			 backgroundColor: 'rgba(0,0,0,0.8)',
			 titleFontSize: 15,
		 },
		responsive: true,
		maintainAspectRatio: false,
		plugins: { 
			legend: {
					labels: { font: {size: 15} }
					},

		},
		title: {
			display: true,
			text: data.cargo.title
		},
		scales : { y: { ticks: {
							font: { size: 15 }, 
							},
					   stacked: true,
					   scaleLabel: {
							display: true,
							labelString: data.Ylabel,
							//fontSize: 30,
							},
					  suggestedMin: 0,
					  suggestedMax: data.y_max
				  },
				  x: { ticks: {
							font: { size: 15 },
					  },
				      //stacked: true
				      }
		         },
	 }
});	
  return new_line_chart;
}

function create_line_chart_cumul(ctx, data){
  var new_line_chart_cumul = new Chart(ctx, {
	type: 'line',
	data: data.cargo,
	options: {
	  responsive: true,
	  showTooltips: true,
	  maintainAspectRatio: false,
	  plugins: { 
		legend: {
				labels: { font: {size: 15} }
				},
		tooltip: { enabled: true}
	  },
	  title: {
		display: true,
		text: data.title
	  },
	scales : { y: { ticks: {
							font: { size: 15 },
								},
					stacked: true,
					scaleLabel: {
						display: true,
						labelString: data.cargo,
						//fontSize: 30,
							},
					 suggestedMin: 0,
					},
				x: { ticks: {
							font: { size: 15 },
						},
					stacked: true
				}
	},


	}
  });
  return new_line_chart_cumul;
}

function create_pie_chart(ctx, data){
  var new_pie_chart = new Chart(ctx, {
	type: 'pie',
	data: {
	  labels: data.labels,
	  datasets: [{
		label: gettext('Percent of words by status'),
		backgroundColor: data.color,
		data: data.data
	  }]          
	},
	options: {
	  responsive: false,
	  legend: {
		position: 'top',
	  },
	  title: {
		display: true,
		text: data.title
	  }
	}
  });
  return new_pie_chart;
}

$(function () {

/* the line chart of the words saved number per week */
var $chart_wordnumber = $("#chart-wordnumber");
$.ajax({
	url: $chart_wordnumber.data("url"),
	success: function (data) {
		if (data.data == 'EMPTY'){
			$chart_wordnumber.html(gettext('Nothing to display'));
		} else {
		  var ctx = $chart_wordnumber[0].getContext("2d");
		  new_line_chart = create_line_chart(ctx, data);
		}
	}
});

/* the line chart of the words saved number */
var $chart_wordnumber_cumul = $("#chart-wordnumber_cumul");
$.ajax({
	url: $chart_wordnumber_cumul.data("url"),
	success: function (data) {
		if (data.data == 'EMPTY'){
			$chart_wordnumber_cumul.html(gettext('Nothing to display'));
		} else {
		  var ctx = $chart_wordnumber_cumul[0].getContext("2d");
		  new_line_chart_cumul = create_line_chart_cumul(ctx, data);
		}
	}
});

/* the Pie chart of the words statuses */
var $chart_statusnumber = $("#chart-statusnumber");
$.ajax({
	url: $chart_statusnumber.data("url"),
	success: function (data) {
		  var ctx = $chart_statusnumber[0].getContext("2d");
		  new_pie_chart = create_pie_chart(ctx, data);
	}
});
});

function check_all(){
	// if click on 'all languages', it checks all the languages:
	$.each($("#ul_language input:not(:checked)"), function(){
		$(this).prop('checked', true);	
	});
	ajax_filterlangform_submit();
	$('#ul_language button').removeClass('active');
}

function ajax_filterlangform_submit(){
	// get what are the checkbox checked for: language and active time
	var chosen_activetime = $("#ul_activetime input:checked").val();

	var chosen_lang = [];
	$.each($("#ul_language input:checked"), function(){
		chosen_lang.push(parseInt($(this).val()));
	});
	// stringify them
	var chosen_lang_json = JSON.stringify(chosen_lang);
	var chosen_activetime_json = JSON.stringify(chosen_activetime);

	var data_to_go = new FormData(); // indispensable to send by POST
	data_to_go.append('lang_filter', chosen_lang_json);
	data_to_go.append('activetime_filter', chosen_activetime_json);

	// get the csrf token
	var token =  $('#chart_filtering_form').find('input[name=csrfmiddlewaretoken]').val(); // Indispensable. Get the csrf already defined in the form
	data_to_go.append('csrfmiddlewaretoken', token);

	$.ajax({url: '/statistics/line_chart/', 
	    type: 'POST',
		cache: false,
		processData: false,
		contentType: false,
		data:  data_to_go,
		success: function(data){ 
			/* drawing the line char */
			/* first we must delete the previous chart: https://stackoverflow.com/questions/40056555/destroy-chart-js-bar-graph-to-redraw-other-graph-in-same-canvas */
			if (typeof new_line_chart != 'undefined'){
				new_line_chart.destroy();
			}
			/* display the line chart non-cumul and cumul and the pie chart */
			var chart_wordnumber = document.getElementById("chart-wordnumber");
			var ctx = chart_wordnumber.getContext("2d");    
			new_line_chart = create_line_chart(ctx, data['noncumulative_data']);

			/* drawing the line char cumulative */
			/* first we must delete the previous chart: https://stackoverflow.com/questions/40056555/destroy-chart-js-bar-graph-to-redraw-other-graph-in-same-canvas */
			if (typeof new_line_chart_cumul != 'undefined'){
				new_line_chart_cumul.destroy();
			}
			/* display the line chart non-cumul and cumul and the pie chart */
			var chart_wordnumber_cumul = document.getElementById("chart-wordnumber_cumul");
			var ctx = chart_wordnumber_cumul.getContext("2d");    
			new_line_chart_cumul = create_line_chart_cumul(ctx, data['cumulative_data']);
		},
		error : function(data , status , xhr){ console.log('ERROR');//error console.log(data); console.log(status); console.log(xhr);
		}
	});

	$.ajax({url: '/statistics/pie_chart/', 
	    type: 'POST',
		cache: false,
		processData: false,
		contentType: false,
		data:  data_to_go,
		success: function(data){ 
			/* drawing the pie char */
			/* first we must delete the previous chart: https://stackoverflow.com/questions/40056555/destroy-chart-js-bar-graph-to-redraw-other-graph-in-same-canvas */
			if (typeof new_pie_chart != 'undefined'){
				new_pie_chart.destroy();
			}
			/* display the line chart non-cumul and cumul and the pie chart */
			var chart_statusnumber = document.getElementById("chart-statusnumber");
			var ctx = chart_statusnumber.getContext("2d");    
			new_pie_chart = create_pie_chart(ctx, data);
		},
		error : function(data , status , xhr){ console.log('ERROR');//error console.log(data); console.log(status); console.log(xhr);
		}
	});
}
